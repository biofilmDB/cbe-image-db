from images import forms, models
import django.views.generic as genViews
from template_names import TemplateNames
from images import search_utils as su


class AboutSite(TemplateNames, genViews.TemplateView):
    pass


class AddImagerView(genViews.CreateView):
    """ Allows a user to ad an imager using a webpage. It uses a genaric create
    model template."""
    template_name = 'images/create_model.html'
    form_class = forms.AddImagerForm
    model = models.Imager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading1'] = "Add a new Imager"
        context['intro_p'] = "Type your name into the box to add yourself as "
        context['intro_p'] += "an imager."
        context['button_text'] = "Add"
        return context


class ImagerSuccessView(TemplateNames, genViews.DetailView):
    model = models.Imager


class ImageDetailsView(TemplateNames, genViews.DetailView):
    """ Shows the details of an image. It is where a sucessfull image upload is
    redirected to."""
    model = models.Image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the image
        image = kwargs['object']
        context['get_image_details'] = su.get_html_image_list(image)
        return context
