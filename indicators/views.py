from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from CultureAnalyzer.settings.default import ITEMS_ON_PAGE
from .models import CountryIndicator
from .forms import CountryIndicatorForm

__all__ = ['CountryIndicatorListView', 'CountryIndicatorCreate',
           'CountryIndicatorDelete', 'CountryIndicatorUpdate']


class CountryIndicatorListView(LoginRequiredMixin, PermissionRequiredMixin,
                               ListView):
    model = CountryIndicator
    template_name = 'indicators/list.html'
    context_object_name = 'indicators'
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'indicators.view_countryindicator'


class CountryIndicatorCreate(LoginRequiredMixin, PermissionRequiredMixin,
                             SuccessMessageMixin,
                             CreateView):
    model = CountryIndicator
    form_class = CountryIndicatorForm
    template_name = 'indicators/create_update.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was created successfully'
    permission_required = 'indicators.add_countryindicator'


class CountryIndicatorDelete(LoginRequiredMixin, PermissionRequiredMixin,
                             SuccessMessageMixin,
                             DeleteView):
    model = CountryIndicator
    context_object_name = 'indicator'
    template_name = 'indicators/delete.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was deleted successfully'
    permission_required = 'indicators.delete_countryindicator'


class CountryIndicatorUpdate(LoginRequiredMixin, PermissionRequiredMixin,
                             SuccessMessageMixin,
                             UpdateView):
    model = CountryIndicator
    form_class = CountryIndicatorForm
    template_name = 'indicators/create_update.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was updated successfully'
    permission_required = 'indicators.change_countryindicator'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context
