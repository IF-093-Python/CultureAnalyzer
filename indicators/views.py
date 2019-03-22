from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q

from CultureAnalyzer.constants import ITEMS_ON_PAGE
from CultureAnalyzer.mixins import SafePaginationMixin
from indicators.models import CountryIndicator
from indicators.forms import CountryIndicatorForm

__all__ = ['CountryIndicatorListView', 'CountryIndicatorCreate',
           'CountryIndicatorDelete', 'CountryIndicatorUpdate']


class CountryIndicatorListView(LoginRequiredMixin, PermissionRequiredMixin,
                               SafePaginationMixin, ListView):
    model = CountryIndicator
    template_name = 'indicators/list.html'
    context_object_name = 'indicators'
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'indicators.view_countryindicator'

    def get_queryset(self):
        indicators = CountryIndicator.objects.all().order_by('iso_code',
                                                             'name')
        indicator_search = self.request.GET.get("indicator_search")
        if indicator_search:
            return indicators.filter(
                Q(iso_code__icontains=indicator_search) |
                Q(name__icontains=indicator_search))
        return indicators

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search'] = self.request.GET.get("indicator_search")
        return context


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
