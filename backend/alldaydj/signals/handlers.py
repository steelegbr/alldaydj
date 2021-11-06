"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.core.files.storage import default_storage
from alldaydj.models import Cart
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created


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


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    # Render the reset email

    render_context = {
        "full_name": reset_password_token.user.get_full_name(),
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "url": f"https://{settings.DOMAIN}/password-reset/{reset_password_token.key}",
    }

    email_html = render_to_string("email/reset_password.html", render_context)
    email_plain = render_to_string("email/reset_password.txt", render_context)

    # Send it

    message = EmailMultiAlternatives(
        settings.PASSWORD_RESET_SUBJECT,
        email_plain,
        settings.DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email],
    )
    message.attach_alternative(email_html, "text/html")
    message.send()


@receiver(post_delete, sender=Cart)
def delete_audio(sender, instance, **kwargs):
    if instance:
        files_to_delete = [f"audio/{instance.id}", f"compressed/{instance.id}"]

        for file in files_to_delete:
            if default_storage.exists(file):
                default_storage.delete(file)
