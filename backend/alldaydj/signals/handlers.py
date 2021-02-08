from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry


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

    if app_label == "alldaydj":
        if model_name == "Cart":
            registry.update(instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs["instance"]

    if app_label == "alldaydj":
        if model_name == "Cart":
            registry.delete(instance, raise_on_error=False)