from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('upload-image/', views.UploadImageView.as_view(), name='upload'),
    path('add-imager/', views.AddImagerView.as_view(), name='add_imager'),
    path('details/<int:pk>/', views.ImageDetailsView.as_view(),
         name='image_details'),
    # Searching and results urls
    path('general-search/', views.GeneralSearchView.as_view(),
         name='general_search'),
    path('search-results/', views.GeneralSearchResultsView.as_view(),
         name='general_search_results'),
    path('search-labs/', views.SearchImageView.as_view(),
         name='search_by_lab'),
    path('view-by-lab/', views.ImageThumbnailsView.as_view(),
         name='view_by_lab'),
    # Autocomplete urls
    path('microscope-autocomplete/',
         views.MicroscopeSettingAutocomplete.as_view(),
         name='microscope_autocomplete'),
    path('imager-autocomplete/', views.ImagerAutocomplete.as_view(),
         name='imager_autocomplete'),
    path('lab-autocomplete/', views.LabAutocomplete.as_view(),
         name='lab_autocomplete'),
    path('search-autocomplete/', views.SearchAutocomplete.as_view(),
         name='search_autocomplete'),
]
