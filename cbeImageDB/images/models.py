from django.db import models
from django.dispatch import receiver


class Lab(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    brief_description = models.CharField(max_length=1000)
    date = models.DateField(("Date"), auto_now_add=True)
    document = models.FileField()
    # TODO: Add path. It worked in the terminal
    # path = document.path
    # image_name = document.name


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
