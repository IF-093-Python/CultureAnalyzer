from django.views.generic.list import ListView
from feedbacks.models import Feedback


class FeedbackListView(ListView):
    model = Feedback
    paginate_by = 10
