"""
    Async tasks for AllDay DJ.
"""

from alldaydj.models import AudioUploadJob
from alldaydj.users.models import TenantUser
from alldaydj.tenants.models import Tenant
from alldaydj.audio import (
    FileStage,
    WaveCompression,
    get_wave_compression,
    generate_file_name,
)
from alldaydj.codecs import get_decoder
from celery import shared_task
from chunk import Chunk
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.storage import default_storage
from django_tenants.utils import tenant_context
from logging import getLogger
import magic
from os import environ
from tenant_users.tenants.tasks import provision_tenant
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.models import ExistsError, UserTenantPermissions
from typing import Any, List, Tuple


@shared_task
def bootstrap(
    public_tenancy_name: str, admin_username: str, admin_password: str
) -> str:
    """
    Bootstraps the public tenancy.

    Args:
        public_tenancy_name (str): The name of the public tenancy.
        admin_username (str): The admin username. Must be an e-mail address.
        admin_password (str): The admin password.
    """

    create_public_tenant(
        f"{public_tenancy_name}.{environ.get('ADDJ_USERS_DOMAIN')}", admin_username
    )

    admin_user = TenantUser.objects.filter(email=admin_username).first()
    admin_user.set_password(admin_password)
    admin_user.save()

    # Continue into making the user a god

    make_superuser.apply_async(args=(admin_username, "Public Tenant", True, True))

    return f"Successfully bootstrapped the {public_tenancy_name} public tenancy with {admin_username}."


@shared_task
def create_tenant(tenant_name: str, username: str) -> str:
    """
    Creates a new tenant.

    Args:
        tenant_name (str): The name / slug for the tenant.
        username (str): The username for the owner.
    """

    provision_tenant(tenant_name, tenant_name, username)
    make_superuser.apply_async(args=(username, tenant_name, True, True))
    return f"Successfully created the {tenant_name} tenancy."


@shared_task
def create_user(email: str, password: str) -> str:
    """Create a user.

    Args:
        email (str): The e-mail address.
        password (str): The password.
    """

    TenantUser.objects.create_user(email=email, password=password)
    return f"Successfully created the {email} user."


def __set_tenant_permissions(
    user: Any, tenant: Any, superuser: bool, staff: bool
) -> None:
    """Sets the specified user permissions on a tenant.

    Args:
        user (Any): The user to set the permissions for.
        tenant (Any): The tenant to set the permissions on.
        superuser (bool): Indicates if the user should be a superuser.
        staff (bool): Indicates if the user should be staff.
    """
    with tenant_context(tenant):

        permission = UserTenantPermissions.objects.get(profile=user)

        if permission:
            permission.is_staff = staff
            permission.is_superuser = superuser
            permission.save()
        else:
            UserTenantPermissions.objects.get_or_create(
                profile=user, is_staff=staff, is_superuser=superuser
            )


@shared_task
def make_superuser(email: str, tenant_name: str, staff: bool, superuser: bool) -> str:
    """Makes a user a superuser.

    Args:
        email (str): The e-mail address of the user to upgrade.
        tenant_name (str): Optional - indicates if we should restrict to a specific tenant.
        staff (bool): Indicates if the staff privilege is needed.
        superuser (bool): Indicates if the superuser privilege is needed.
    """

    # Find the user

    user = TenantUser.objects.filter(email=email).first()
    if not user:
        raise ValueError(f"Could not find user {email}.")

    if tenant_name:

        # Specific tenancy

        tenant = Tenant.objects.filter(name=tenant_name).first()
        if not tenant:
            raise ValueError(f"Could not find tenant {tenant_name}.")

        # Set the permissions

        __set_tenant_permissions(user, tenant, staff, superuser)

        return f"Successfully applied permissions for {user} on the {tenant} tenancy."

    # Every tenancy

    tenants = Tenant.objects.all()
    for tenant in tenants:
        __set_tenant_permissions(user, tenant, staff, superuser)

    return f"Successfully applied permissions for {user} on all tenancies."


@shared_task
def set_tenant_user_permissions(
    username: str, tenancy: str, permissions: List[str]
) -> str:
    """
    Sets the permissions for a given user in a specified tenancy.

    Args:
        username (str): The username to set the permissions for.
        tenancy (str): The tenancy to set the permissions on.
        permissions (List[str]): The permissions to set.
    """

    # Find the user

    user = TenantUser.objects.filter(email=username).first()
    if not user:
        raise ValueError(f"Failed to find user {username}.")

    # Find the tenancy

    tenant = Tenant.objects.filter(name=tenancy).first()
    if not tenant:
        raise ValueError(f"Failed to find the {tenancy} tenancy.")

    # Apply the permissions

    with tenant_context(tenant):
        (user_permissions, _) = UserTenantPermissions.objects.get_or_create(
            profile=user
        )

        for permission in permissions:
            current_permission = Permission.objects.get(codename=permission)
            user_permissions.user_permissions.add(current_permission)

        user_permissions.save()

    return f"Successfully updated permissions for {username} in {tenancy}."


@shared_task
def join_user_tenancy(username: str, tenancy: str) -> str:
    """
    Joins a specific user to a tenancy with default permissions.

    Args:
        username (str): The user to join.
        tenancy (str): The name of the tenancy.
    """

    # Find the user

    user = TenantUser.objects.filter(email=username).first()
    if not user:
        raise ValueError(f"Failed to find user {username}.")

    # Find the tenancy

    tenant = Tenant.objects.filter(name=tenancy).first()
    if not tenant:
        raise ValueError(f"Failed to find the {tenancy} tenancy.")

    # Make the magic happen

    try:
        tenant.add_user(user)
    except ExistsError:
        # Silently ignore if it's already done
        pass

    # Set the default permissions

    set_tenant_user_permissions.apply_async(
        args=(username, tenancy, settings.ADDJ_DEFAULT_PERMISSIONS)
    )

    return f"Successfully added {username} to the {tenancy} tenancy."


def __get_upload_job(job_id: str, tenant_name: str) -> Tuple[Tenant, AudioUploadJob]:
    """
    Obtains the upload job and associated tenancy.

    Args:
        job_id (str): The job ID to search for.
        tenant_name (str): The tenant this should be attached to.

    Raises:
        ValueError: Failed to get the tenant or job.

    Returns:
        Tuple[Tenant, AudioUploadJob]: The tenant and the job.
    """

    # Switch into the correct tenancy

    tenant = Tenant.objects.filter(name=tenant_name).first()
    if not tenant:
        raise ValueError(f"{tenant_name} is not a valid tenancy.")

    # Find the upload job

    with tenant_context(tenant):
        job = AudioUploadJob.objects.filter(id=job_id).first()

    if not job:
        raise ValueError(f"Upload job {job_id} on tenant {tenant} is not valid.")

    return (tenant, job)


def __set_job_status(
    job_id: str, tenant_name: str, status: AudioUploadJob.AudioUploadStatus
) -> Tuple[Tenant, AudioUploadJob]:
    """
    Sets the audio upload job status.

    Args:
        job_id (str): The UUID of the job.
        tenant_name (str): The tenant the job is for.
        status (AudioUploadJob.AudioUploadStatus): The status to set.

    Returns:
        Tuple[Tenant, AudioUploadJob]: The tenant and the job.
    """

    (tenant, job) = __get_upload_job(job_id, tenant_name)
    job.status = status
    job.save()

    return (tenant, job)


def _set_job_error(job: AudioUploadJob, error: str) -> str:
    """
    Sets the error on the audio upload job.

    Args:
        job (AudioUploadJob): The job to set the error on.
        error (str): The error message.
    """

    job.status = AudioUploadJob.AudioUploadStatus.ERROR
    job.error = error
    job.save()
    return error


def _move_audio_file(src: str, dst: str):
    """
    Moves an audio file in the django file store.

    Args:
        src (str): The source file name.
        dst (str): The destination file name.
    """

    # Check the source exists

    if not default_storage.exists(src):
        raise ValueError(f"{src} is not a valid source file name.")

    # Copy the contents

    with default_storage.open(src, "rb") as src_file:
        contents = src_file.read()

    default_storage.save(dst, contents)

    # Delete the source file

    default_storage.delete(src)


@shared_task
def validate_audio_upload(job_id: str, tenant_name: str) -> str:
    """
    Validates an uploaded audio file.

    Args:
        job_id (str): The UUID of the job we're working on.
        tenant_name (str): The name of the tenant this task it running under.

    Returns:
        str: The success / failure message.
    """

    (tenant, job) = __set_job_status(
        job_id, tenant_name, AudioUploadJob.AudioUploadStatus.VALIDATING
    )

    # Open the file and check the type

    inbound_file_name = generate_file_name(job, tenant, FileStage.QUEUED)
    uncompressed_file_name = generate_file_name(job, tenant, FileStage.AUDIO)

    with default_storage.open(inbound_file_name, "rb") as inbound_file:
        mime = magic.from_buffer(inbound_file.read(1024))
        inbound_file.seek(0)

    if mime == "audio/wav":

        # WAVE files - need to check if it's compressed

        with default_storage.open(inbound_file_name, "rb") as inbound_file:
            compression = get_wave_compression(inbound_file)

        if compression == WaveCompression.COMPRESSED:
            return _set_job_error(job, "Compressed WAVE files are not supported.")
        elif compression == WaveCompression.UNCOMPRESSED:
            _move_audio_file(inbound_file_name, uncompressed_file_name)
        elif compression == WaveCompression.INVALID:
            return _set_job_error(job, "Failed to find the format chunk.")

    elif any(mime_type in mime for mime_type in settings.ADDJ_COMPRESSED_MIME_TYPES):

        # Compressed files - re-encode

        decompress_audio.apply_async(args=(job_id, tenant_name))

    else:

        # Invalid format
        # Delete the file and note the error in the job

        default_storage.delete(inbound_file_name)
        return _set_job_error(job, f"{mime} is not a valid audio file MIME type.")


@shared_task
def decompress_audio(job_id: str, tenant_name: str, mime: str):
    """
    Decompresses audio to WAVE format.

    Args:
        job_id (str): The job to perform this task for.
        tenant (str): The tenant to perform this task for.
        mime (str): The mime type of the file.
    """

    (tenant, job) = __set_job_status(
        job_id, tenant_name, AudioUploadJob.AudioUploadStatus.DECOMPRESSING
    )
    logger = getLogger(__name__)

    # Open the files and attempt to convert

    inbound_file_name = generate_file_name(job, tenant, FileStage.QUEUED)
    uncompressed_file_name = generate_file_name(job, tenant, FileStage.AUDIO)

    with default_storage.open(inbound_file_name) as inbound_file, default_storage.open(
        uncompressed_file_name
    ) as uncompressed_file:

        try:
            get_decoder(mime).decode(inbound_file, uncompressed_file)
        except Exception as ex:
            logger.error(
                f"Failed to decompress the audio for upload job {job_id} on tenant {tenant_name}.",
                ex,
            )
            return _set_job_error(job, "Failed to decompress the audio.")


@shared_task
def extract_audio_metadata(job_id: str, tenant: str):
    """
    Attempts to extract metadata from an uncompressed audio file.

    Args:
        job_id (str): The job to perform this task for.
        tenant (str): The tenant to perform this task for.
    """

    pass
