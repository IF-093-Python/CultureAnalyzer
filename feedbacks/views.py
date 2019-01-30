from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from CultureAnalyzer.settings.base_settings import ITEMS_ON_PAGE
from CultureAnalyzer.paginator import SafePaginator
from feedbacks.models import Feedback, Recommendation
from .forms import FeedbackForm


class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    paginator_class = SafePaginator
    paginate_by = ITEMS_ON_PAGE
    context_object_name = 'feedbacks'
    ordering = ['id']


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


class RecommendationListView(LoginRequiredMixin, ListView):
    model = Recommendation
    paginator_class = SafePaginator
    paginate_by = ITEMS_ON_PAGE
    context_object_name = 'recommendations'
    ordering = ['feedback', 'id']


class RecommendationDeleteView(LoginRequiredMixin, DeleteView):
    model = Recommendation
    success_url = reverse_lazy('recommendation-list')


class RecommendationCreateView(LoginRequiredMixin, CreateView):
    model = Recommendation
    fields = ('feedback', 'recommendation')


class RecommendationUpdateView(LoginRequiredMixin, UpdateView):
    model = Recommendation
    fields = ('feedback', 'recommendation')
    template_name_suffix = '_form'
