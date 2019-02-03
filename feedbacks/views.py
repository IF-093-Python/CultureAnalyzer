from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from CultureAnalyzer.settings.base_settings import ITEMS_ON_PAGE
from CultureAnalyzer.view import SafePaginationListView
from feedbacks.models import Feedback, Recommendation
from feedbacks.forms import FeedbackForm, RecommendationForm


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
        back = self.get_object().feedback.id
        self.success_url = reverse_lazy('feedback-detail', kwargs={'pk': back})
        print(back)
        return super().delete(self, request, *args, **kwargs)


class RecommendationCreateView(LoginRequiredMixin, CreateView):
    model = Recommendation
    fields = ('feedback', 'recommendation')
    form_class = RecommendationForm
    feed = None

    def get(self, request, feedback, *args, **kwargs):
        """Get feedback id from url"""
        self.feed = feedback
        return super().get(request, *args, **kwargs)

    def get_form(self, **kwargs):
        """Give feedback id to form"""
        return self.form_class(self.feed, **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        """Redirect to linked feedback"""
        back = self.get_form().data.get('feedback')
        self.success_url = reverse_lazy('feedback-detail', kwargs={'pk': back})
        return super().post(self, request, *args, **kwargs)


class RecommendationUpdateView(LoginRequiredMixin, UpdateView):
    model = Recommendation
    fields = ('feedback', 'recommendation')
    template_name_suffix = '_form'
    success_url = reverse_lazy('feedback-list')

    def post(self, request, *args, **kwargs):
        """Redirect to linked feedback"""
        back = self.get_form().data.get('feedback')
        self.success_url = reverse_lazy('feedback-detail', kwargs={'pk': back})
        return super().post(self, request, *args, **kwargs)
