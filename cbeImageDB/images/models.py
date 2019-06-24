from django.db import models
from django.dispatch import receiver
from datetime import date


class Objective(models.Model):
    objective = models.CharField(max_length=10)
    medium = models.CharField(max_length=20)

    def __str__(self):
        return '{} {}'.format(self.objective, self.medium)


class Microscope(models.Model):
    microscope_name = models.CharField(max_length=500)
    objective = models.ForeignKey(Objective, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.microscope_name, str(self.objective))


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
    microscope = models.ForeignKey(Microscope, on_delete=models.PROTECT)
    brief_description = models.CharField(max_length=1000)
    date = models.DateField(("Date"), default=date.today)
    document = models.ImageField(upload_to=imager_directory_path)

    def __str__(self):
        return str(self.document.name)


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
