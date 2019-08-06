from django.contrib import admin
from .models import Lab, Microscope_settings, Medium
from django.http import HttpResponseRedirect
from django.urls import reverse
from admin_views.admin import AdminViews


class AdminSearch(AdminViews):
    admin_views = (
                    ('General Search', 'redirect_to_general'),
                    ('Attribute Search', 'redirect_to_attribute'),
        )

    def redirect_to_general(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('images:general_search'))

    def redirect_to_attribute(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('images:attribute_search'))


admin.site.register(Medium)
admin.site.register(Lab, AdminSearch)
admin.site.register(Microscope_settings)
