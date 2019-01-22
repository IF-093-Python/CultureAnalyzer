from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import CountryIndicator
from .forms import CountryIndicatorForm


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


@login_required
def country_indicator_update(request, pk):

    """Update country indicator. Delete and create new record.
    If form isn't valid restore with previous fields 
    record into db."""

    country_indicator_obj = get_object_or_404(CountryIndicator, pk=pk)
    tmp_pk = country_indicator_obj.pk
    deleted_object = False
    if request.method == 'POST':
        form = CountryIndicatorForm(request.POST)
        country_indicator_obj.delete()
        deleted_object = True
        country_indicator_obj.pk = tmp_pk
        if form.is_valid():
            current_country_indicator = form.save(commit=False)
            try:
                iso_code = request.POST['iso_code']
                current_country_indicator.pk = iso_code
                current_country_indicator.save()
            except KeyError:
                raise Http404

            messages.success(request, f'Country indicator: '
                             f'{current_country_indicator.name} was'
                             f' updated successfully')
            return redirect("country_indicator:country_indicator_list")
    else:
        form = CountryIndicatorForm(instance=country_indicator_obj)
    if deleted_object:
        country_indicator_obj.save()
    update = True
    return render(request, "indicators/create_update.html", {
        'update': update,
        'form': form,
                })


class CountryIndicatorDelete(LoginRequiredMixin, SuccessMessageMixin,
                             DeleteView):
    model = CountryIndicator
    context_object_name = 'indicator'
    template_name = 'indicators/delete.html'
    success_url = reverse_lazy('country_indicator:country_indicator_list')
    success_message = 'Country indicator: "%(name)s" was deleted successfully'

