from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('upload-image/', views.upload_file, name='upload'),
    path('<int:pk>/success/', views.ImageDetailsView.as_view(),
         name='image_details'),
    path('view_by_lab/', views.ImageThumbnailsView.as_view(),
         name='view_by_lab'),
]
