from django.db import models
from django.dispatch import receiver
from datetime import date
import os
from django.conf import settings


class Microscope(models.Model):
    microscope_name = models.CharField(max_length=500)

    def __str__(self):
        return self.microscope_name


class Medium(models.Model):
    medium_type = models.CharField(max_length=50)

    def __str__(self):
        return self.medium_type


class Microscope_settings(models.Model):
    microscope = models.ForeignKey(Microscope, on_delete=models.PROTECT)
    objective = models.FloatField()
    medium = models.ForeignKey(Medium, on_delete=models.PROTECT)

    def __str__(self):
        if self.objective.is_integer():
            obj = int(self.objective)
        else:
            obj = self.objective
        return '{} {}x {}'.format(self.microscope, obj, self.medium)


class Lab(models.Model):
    pi_name = models.CharField(max_length=100)

    def __str__(self):
            return self.pi_name


class Imager(models.Model):
    imager_name = models.CharField(max_length=100)

    def __str__(self):
        return self.imager_name


def imager_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    formated_imager = str(instance.imager).replace(' ', '_')
    filename = filename.replace(' ', '_')
    return '{0}/{1}'.format(formated_imager, filename)


class Image(models.Model):
    # With ForeignKey on_delete was PROTECT
    lab = models.ManyToManyField(Lab)
    imager = models.ForeignKey(Imager, on_delete=models.PROTECT)
    microscope_setting = models.ForeignKey(Microscope_settings,
                                           on_delete=models.PROTECT)
    brief_description = models.CharField(max_length=1000)
    date = models.DateField(("Date"), default=date.today)
    document = models.ImageField(upload_to=imager_directory_path)

    def __str__(self):
        return str(self.document.name)


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    name = instance.document.name.split('/')[-1]
    loc = '/' + instance.document.name.split('/')[0]
    matching_files = []
    instance.document.delete(save=False)
    for root, dirs, files in os.walk(settings.MEDIA_ROOT + loc):
        for f in files:
            if name in f:
                f = '/'.join([root, f])
                matching_files.append(f)
        break
    for f in matching_files:
        try:
            os.remove(f)
        except FileNotFoundError:
            print('File not found while tyring to delete a thumbnail: {}'.format(f))
