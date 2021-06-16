from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_elasticsearch_dsl.registries import registry
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


@receiver(post_save)
def update_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs["instance"]

    if app_label == "alldaydj" and model_name == "Cart":
        registry.update(instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs["instance"]

    if app_label == "alldaydj" and model_name == "Cart":
        registry.delete(instance, raise_on_error=False)


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
