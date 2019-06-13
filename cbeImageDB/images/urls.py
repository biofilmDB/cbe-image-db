from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('upload_image/', views.upload_file, name='upload'),
    path('add_imager/', views.AddImagerView.as_view(), name='add_imager'),
    path('<int:pk>/success/', views.ImageDetailsView.as_view(),
         name='image_details'),
    path('search_labs', views.SearchImageView.as_view(), name='search_by_lab'),
    path('view_by_lab/', views.ImageThumbnailsView.as_view(),
         name='view_by_lab'),
]
