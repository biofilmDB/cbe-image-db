from django.db import models
from django.dispatch import receiver


class Lab(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    image_name = models.CharField(max_length=500)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    document = models.FileField()
    path = document.path


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
