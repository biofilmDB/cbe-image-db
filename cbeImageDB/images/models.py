from django.db import models
from django.dispatch import receiver


class Lab(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
            return self.name


def lab_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    formated_lab = str(instance.lab).replace(' ', '_')
    return '{0}/{1}'.format(formated_lab, filename)


class Image(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.PROTECT)
    brief_description = models.CharField(max_length=1000)
    date = models.DateField(("Date"), auto_now_add=True)
    document = models.ImageField(upload_to=lab_directory_path)
    path = models.CharField(max_length=500)
    image_name = models.CharField(max_length=100)

    def __str__(self):
        return self.image_name


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
