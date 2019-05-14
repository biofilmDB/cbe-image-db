from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('upload-image/', views.upload_file, name='upload'),
    ]
