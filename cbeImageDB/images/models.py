from django.db import models
from django.dispatch import receiver


class Lab(models.Model):
    pi_name = models.CharField(max_length=100)

    def __str__(self):
            return self.pi_name


class Imager(models.Model):
    imager_name = models.CharField(max_length=100)

    def __str__(self):
        return self.imager_name


def lab_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    formated_lab = str(instance.lab).replace(' ', '_')
    filename = filename.replace(' ', '_')
    return '{0}/{1}'.format(formated_lab, filename)


class Image(models.Model):
    # With ForeighnKey on_delete was PROTECT
    lab = models.ManyToManyField(Lab)
    imager = models.ForeignKey(Imager, on_delete=models.PROTECT)
    brief_description = models.CharField(max_length=1000)
    date = models.DateField(("Date"), auto_now_add=True)
    document = models.ImageField(upload_to=lab_directory_path)

    def __str__(self):
        return str(self.document.name)


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
