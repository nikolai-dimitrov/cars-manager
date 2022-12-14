from cloudinary import uploader
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from cars.ad.models import Ad


@receiver(pre_delete, sender=Ad)
def ad_pre_delete_images(sender, instance, *args, **kwargs):
    uploader.destroy(f'cars/{instance.get_title}_image_main')
    uploader.destroy(f'cars/{instance.get_title}_image1')
    uploader.destroy(f'cars/{instance.get_title}_image2')
    uploader.destroy(f'cars/{instance.get_title}_image3')
