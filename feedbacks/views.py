from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.urls import reverse_lazy

from CultureAnalyzer.settings.default import ITEMS_ON_PAGE
from CultureAnalyzer.view import SafePaginationListView
from feedbacks.models import Feedback, Recommendation
from feedbacks.forms import FeedbackForm, RecommendationForm

__all__ = ['FeedbackListView', 'FeedbackCreateView', 'FeedbackUpdateView',
           'FeedbackDeleteView', 'FeedbackDetailView',
           'RecommendationCreateView', 'RecommendationUpdateView',
           'RecommendationDeleteView', ]


class FeedbackListView(LoginRequiredMixin, PermissionRequiredMixin,
                       SafePaginationListView):
    model = Feedback
    paginate_by = ITEMS_ON_PAGE
    context_object_name = 'feedbacks'
    ordering = ['id']
    permission_required = 'view_feedback'


class FeedbackDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                         DetailView):
    model = Feedback
    permission_required = 'view_feedback'


class FeedbackDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                         DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback-list')
    permission_required = 'delete_feedback'


class FeedbackCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                         CreateView):
    model = Feedback
    form_class = FeedbackForm
    permission_required = 'add_feedback'


class FeedbackUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                         UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name_suffix = '_form'
    permission_required = 'change_feedback'


class RecommendationDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                               DeleteView):
    model = Recommendation
    permission_required = 'delete_recommendation'

    def delete(self, request, *args, **kwargs):
        """Redirect to linked feedback"""
        with transaction.atomic():
            self.success_url = reverse_lazy('feedback-detail', kwargs={
                'pk': self.get_object().feedback.id
                })
            return super().delete(self, request, *args, **kwargs)


class RecommendationCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                               CreateView):
    model = Recommendation
    form_class = RecommendationForm
    permission_required = 'add_recommendation'

    def get(self, request, *args, **kwargs):
        err_result = HttpResponseBadRequest(
            '<h1>Invalid request parameters</h1>')
        try:
            is_exists = Feedback.objects.filter(
                pk=self.request.GET.get('feedback')).exists()
            if not is_exists:
                return err_result
        except (ValueError, TypeError):
            return err_result
        return super().get(request, *args, **kwargs)

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
                                            'pk': request.GET.get('feedback')
                                            })
        return super().post(self, request, *args, **kwargs)


class RecommendationUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                               UpdateView):
    model = Recommendation
    template_name_suffix = '_form'
    form_class = RecommendationForm
    permission_required = 'change_recommendation'

    def get(self, request, *args, **kwargs):
        """Set success_url to linked feedback"""
        self.success_url = reverse_lazy('feedback-detail', kwargs={
            'pk': self.get_object().feedback.id
            })
        return super().get(request, *args, **kwargs)
