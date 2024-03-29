from django.db import models
from django.dispatch import receiver
from datetime import date, timedelta
from easy_thumbnails.fields import ThumbnailerImageField
from django.urls import reverse


class Organism(models.Model):
    name = models.CharField(db_index=True, max_length=1000, unique=True)
    ncbi_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name', ])
        ]


class Microscope(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class ObjectiveMedium(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MicroscopeSettings(models.Model):
    microscope = models.ForeignKey(Microscope, on_delete=models.PROTECT)
    objective = models.FloatField()
    medium = models.ForeignKey(ObjectiveMedium, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('microscope', 'objective', 'medium',)

    def __str__(self):
        if self.objective.is_integer():
            obj = int(self.objective)
        else:
            obj = self.objective
        return '{} {}x {}'.format(self.microscope, obj, self.medium)


class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
            return self.name


class Imager(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('images:imager_success', kwargs={'pk': self.pk})


def imager_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    formated_imager = str(instance.imager).replace(' ', '_')
    filename = filename.replace(' ', '_')
    return '{0}/{1}'.format(formated_imager, filename)


def medium_thumb_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    formated_imager = str(instance.imager).replace(' ', '_')
    filename = filename.split('/')[-1]
    return '{}/thumbs/medium/{}'.format(formated_imager, filename)


def large_thumb_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    formated_imager = str(instance.imager).replace(' ', '_')
    filename = filename.split('/')[-1]
    return '{}/thumbs/large/{}'.format(formated_imager, filename)


class GrowthSubstratum(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Vessel(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('images:project_success', kwargs={'pk': self.pk})


class Experiment(models.Model):
    name = models.CharField(max_length=500, unique=True)
    date_created = models.DateField(("Date created"), default=date.today)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    lab = models.ManyToManyField(Lab, through='ProtectLab')
    organism = models.ManyToManyField(Organism, through='ProtectOrganism')
    vessel = models.ForeignKey(Vessel, on_delete=models.PROTECT)
    substratum = models.ForeignKey(GrowthSubstratum, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    @property
    def is_editable(self):
        # Get today's date
        today = date.today()
        # get the date for tomorrow
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)
        # less than or equal to, so it'll be editable tomorrow as well
        # include yesterday to put a lower limit on it
        return yesterday < self.date_created <= tomorrow


# TODO: Is cascade correct for experiments?
class ProtectLab(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.PROTECT)


class ProtectOrganism(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    organism = models.ForeignKey(Organism, on_delete=models.PROTECT)


class Image(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.PROTECT)
    imager = models.ForeignKey(Imager, on_delete=models.PROTECT)
    microscope_setting = models.ForeignKey(MicroscopeSettings,
                                           on_delete=models.PROTECT)
    date_taken = models.DateField(("Date taken"), default=date.today)
    release_date = models.DateField(("Can't be used before"),
                                    default=date.today)
    date_uploaded = models.DateField(("Date uploaded"), default=date.today)
    document = models.ImageField(upload_to=imager_directory_path)
    brief_description = models.CharField(max_length=1000)
    path_to_raw_data = models.CharField(max_length=500, blank=True, null=True)
    medium_thumb = ThumbnailerImageField(upload_to=medium_thumb_directory_path,
                                         resize_source=dict(size=(200, 200),
                                                            sharpen=True))
    large_thumb = ThumbnailerImageField(upload_to=large_thumb_directory_path,
                                        resize_source=dict(size=(350, 350),
                                                           sharpen=True))

    def __str__(self):
        return str(self.document.name)
    
    @property
    def is_editable(self):
        # Get today's date
        today = date.today()
        # get the date for tomorrow
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)
        # less than or equal to, so it'll be editable tomorrow as well
        # include yesterday to put a lower limit on it
        return yesterday < self.date_uploaded <= tomorrow

    #def save(self, *args, **kwargs):
    #    # TODO: Put thumb saving logic here so it's unform and easier
    #    self.medium_thumb.save(name=self.document.name,
    #                            content=self.document)
    #    self.large_thumb.save(name=self.document.name,
    #                           content=self.document)
    #    super(Image, self).save(*args, **kwargs)  # Call the "real" save() method.


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
    instance.medium_thumb.delete(save=False)
    instance.large_thumb.delete(save=False)
