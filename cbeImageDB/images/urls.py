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
    path('attribute-search/', views.AttributeSearchImageView.as_view(),
         name='attribute_search'),
    path('attribute-results/', views.AttributeSearchResultsView.as_view(),
         name='attribute_search_results'),
    # Autocomplete urls
    path('microscope-setting-autocomplete/',
         views.MicroscopeSettingAutocomplete.as_view(),
         name='microscope_setting_autocomplete'),
    path('microscope-autocomplete/',
         views.MicroscopeAutocomplete.as_view(),
         name='microscope_autocomplete'),
    path('medium-autocomplete/', views.MediumAutocomplete.as_view(),
         name='medium_autocomplete'),
    path('imager-autocomplete/', views.ImagerAutocomplete.as_view(),
         name='imager_autocomplete'),
    path('lab-autocomplete/', views.LabAutocomplete.as_view(),
         name='lab_autocomplete'),
    path('search-autocomplete/', views.SearchAutocomplete.as_view(),
         name='search_autocomplete'),
]
