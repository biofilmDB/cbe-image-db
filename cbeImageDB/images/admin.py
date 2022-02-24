from django.contrib import admin
from images import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from admin_views.admin import AdminViews
# from django.contrib.admin import AdminSite


class AdminSearch(AdminViews):
    admin_views = (
                    ('Upload Image', 'redirect_to_upload'),
                    ('General Search', 'redirect_to_general'),
                    ('Attribute Search', 'redirect_to_attribute'),
        )

    def redirect_to_upload(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('images:upload'))

    def redirect_to_general(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('images:general_search'))

    def redirect_to_attribute(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('images:attribute_search'))

# Things to appear on admin page
admin.site.register(models.MicroscopeSettings)
admin.site.register(models.Microscope)
admin.site.register(models.ObjectiveMedium)
admin.site.register(models.Lab, AdminSearch)
admin.site.register(models.Experiment)
admin.site.register(models.Vessel)
admin.site.register(models.GrowthSubstratum)
admin.site.register(models.Project)
admin.site.register(models.Organism)
