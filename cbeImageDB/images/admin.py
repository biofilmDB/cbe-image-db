from django.contrib import admin
from .models import Lab, Microscope_settings, Medium


admin.site.register(Lab)
admin.site.register(Medium)
admin.site.register(Microscope_settings)
