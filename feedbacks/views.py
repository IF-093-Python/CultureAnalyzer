from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from feedbacks.models import Feedback

ITEMS_ON_PAGE = 5


class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    paginate_by = ITEMS_ON_PAGE
    context_object_name = 'feedbacks'
    ordering = ['id']


class FeedbackDeleteView(LoginRequiredMixin, DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback-list')


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['feedback']


class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    model = Feedback
    fields = ['feedback']
    template_name_suffix = '_form'
