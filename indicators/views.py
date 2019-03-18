from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from CultureAnalyzer.settings.default import ITEMS_ON_PAGE
from indicators.models import CountryIndicator
from indicators.forms import CountryIndicatorForm

__all__ = ['CountryIndicatorListView', 'CountryIndicatorCreate',
           'CountryIndicatorDelete', 'CountryIndicatorUpdate']


class CountryIndicatorListView(LoginRequiredMixin, ListView):
    model = CountryIndicator
    template_name = 'indicators/list.html'
    context_object_name = 'indicators'
    paginate_by = ITEMS_ON_PAGE

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
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get("indicator_search")
        return context


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
