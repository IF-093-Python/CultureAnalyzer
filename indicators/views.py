from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CountryIndicator
from .forms import CountryIndicatorForm
from .custom_update import CustomUpdateView


ITEMS_PER_PAGE = 4


class CountryIndicatorListView(LoginRequiredMixin, ListView):
    model = CountryIndicator
    template_name = 'indicators/list.html'
    context_object_name = 'indicators'
    paginate_by = ITEMS_PER_PAGE


class CountryIndicatorCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
                             CustomUpdateView):
    model = CountryIndicator
    form_class = CountryIndicatorForm
    template_name = 'indicators/create_update.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context
