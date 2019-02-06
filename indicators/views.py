from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from CultureAnalyzer.settings.base_settings import ITEMS_ON_PAGE
from .models import CountryIndicator
from .forms import CountryIndicatorForm

__all__ = ['CountryIndicatorListView', 'CountryIndicatorCreate',
           'CountryIndicatorDelete', 'CountryIndicatorUpdate']


class CountryIndicatorListView(LoginRequiredMixin, ListView):
    model = CountryIndicator
    template_name = 'indicators/list.html'
    context_object_name = 'indicators'
    paginate_by = ITEMS_ON_PAGE


class CountryIndicatorCreate(LoginRequiredMixin, SuccessMessageMixin,
                             CreateView):
    model = CountryIndicator
    form_class = CountryIndicatorForm
    template_name = 'indicators/create_update.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was created successfully'


class CountryIndicatorDelete(LoginRequiredMixin, SuccessMessageMixin,
                             DeleteView):
    model = CountryIndicator
    context_object_name = 'indicator'
    template_name = 'indicators/delete.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was deleted successfully'


class CountryIndicatorUpdate(LoginRequiredMixin, SuccessMessageMixin,
                             UpdateView):
    model = CountryIndicator
    form_class = CountryIndicatorForm
    template_name = 'indicators/create_update.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context
