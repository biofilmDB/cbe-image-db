from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('upload-image/', views.upload_file, name='upload'),
    path('<int:pk>/success/', views.ImageDetailsView.as_view(),
         name='image_details'),
    path('search_labs', views.SearchImageView.as_view(), name='search_by_lab'),
    path('view_by_lab/', views.ImageThumbnailsView.as_view(),
         name='view_by_lab'),
]
