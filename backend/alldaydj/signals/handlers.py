from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_to_default_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name=settings.ADDJ_DEFAULT_GROUP)

        # Update group permissions

        for permission in settings.ADDJ_DEFAULT_PERMISSIONS:
            permission_obj = Permission.objects.get(codename=permission)
            if permission_obj:
                group.permissions.add(permission_obj)

        group.save()

        # Add the user to the group

        instance.groups.add(group)