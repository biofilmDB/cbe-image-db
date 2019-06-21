from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('upload-image/', views.UploadImageView.as_view(), name='upload'),
    path('add_imager/', views.AddImagerView.as_view(), name='add_imager'),
    path('details/<int:pk>/', views.ImageDetailsView.as_view(),
         name='image_details'),
    path('search-labs', views.SearchImageView.as_view(), name='search_by_lab'),
    path('microscope-autocomplete/', views.MicroscopeAutocomplete.as_view(),
         name='microscope_autocomplete'),
    path('imager-autocomplete/', views.ImagerAutocomplete.as_view(),
         name='imager_autocomplete'),
    path('lab-autocomplete/', views.LabAutocomplete.as_view(),
         name='lab_autocomplete'),
    path('view-by-lab/', views.ImageThumbnailsView.as_view(),
         name='view_by_lab'),
]
