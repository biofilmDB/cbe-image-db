from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('upload-image/', views.upload_file, name='upload'),
    path('<int:pk>/success/', views.ImageDetailsView.as_view(),
         name='image_details'),
    ]
