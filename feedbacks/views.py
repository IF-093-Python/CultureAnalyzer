from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from CultureAnalyzer.settings.base_settings import ITEMS_ON_PAGE
from CultureAnalyzer.view import SafePaginationListView
from feedbacks.models import Feedback, Recommendation
from feedbacks.forms import FeedbackForm, RecommendationForm

__all__ = ['FeedbackListView', 'FeedbackCreateView', 'FeedbackUpdateView',
           'FeedbackDeleteView', 'FeedbackDetailView',
           'RecommendationCreateView', 'RecommendationUpdateView',
           'RecommendationDeleteView', ]


class FeedbackListView(LoginRequiredMixin, SafePaginationListView):
    model = Feedback
    paginate_by = ITEMS_ON_PAGE
    context_object_name = 'feedbacks'
    ordering = ['id']


class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = Feedback


class FeedbackDeleteView(LoginRequiredMixin, DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback-list')


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm


class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name_suffix = '_form'


class RecommendationDeleteView(LoginRequiredMixin, DeleteView):
    model = Recommendation

    def delete(self, request, *args, **kwargs):
        """Redirect to linked feedback"""
        with transaction.atomic():
            self.success_url = reverse_lazy('feedback-detail', kwargs={
                'pk': self.get_object().feedback.id})
            return super().delete(self, request, *args, **kwargs)


class RecommendationCreateView(LoginRequiredMixin, CreateView):
    model = Recommendation
    form_class = RecommendationForm

    def get(self, request, *args, **kwargs):
        try:
            Feedback.objects.get(pk=int(self.request.GET.get('feedback')))
        except (ValueError, TypeError, Feedback.DoesNotExist):
            return HttpResponseBadRequest('<h1>Invalid request parameters</h1>')
        return super().get(request, *args, *kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.feedback = Feedback.objects.get(
                pk=self.request.GET.get('feedback'))
            self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """Redirect to linked feedback"""
        self.success_url = reverse_lazy('feedback-detail',
                                        kwargs={
                                            'pk': request.GET.get('feedback')})
        return super().post(self, request, *args, **kwargs)


class RecommendationUpdateView(LoginRequiredMixin, UpdateView):
    model = Recommendation
    template_name_suffix = '_form'
    form_class = RecommendationForm

    def get(self, request, *args, **kwargs):
        """Set success_url to linked feedback"""
        self.success_url = reverse_lazy('feedback-detail', kwargs={
            'pk': self.get_object().feedback.id})
        return super().get(request, *args, **kwargs)
