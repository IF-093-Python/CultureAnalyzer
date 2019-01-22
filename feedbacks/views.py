from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from feedbacks.models import Feedback


class FeedbackListView(ListView):
    model = Feedback


class FeedbackDeleteView(DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback-list')


class FeedbackCreateView(CreateView):
    model = Feedback
    fields = ['feedback']


class FeedbackUpdateView(UpdateView):
    model = Feedback
    fields = ['feedback']
    template_name_suffix = '_form'
