from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from feedbacks.models import Feedback


class FeedbackListView(ListView):
    model = Feedback
    paginate_by = 10


class FeedbackDeleteView(DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback-list')
