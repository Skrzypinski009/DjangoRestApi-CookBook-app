import os
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Recipe


@receiver(post_delete, sender=Recipe)
def delete_recipe_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Recipe)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Recipe.objects.get(pk=instance.pk).image
    except ObjectDoesNotExist:
        return False

    new_file = instance.image
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
