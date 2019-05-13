from django.db import models


class Lab(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
            return self.name


class Image(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    brief_description = models.CharField(max_length=1000)
    date = models.DateField(("Date"), auto_now_add=True)
    document = models.FileField()
    path = models.CharField(max_length=500)
    image_name = models.CharField(max_length=100)


@receiver(models.signals.post_delete, sender=Image)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
