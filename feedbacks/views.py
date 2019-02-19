from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.urls import reverse_lazy

from feedbacks.models import Feedback

ITEMS_ON_PAGE = 5


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            return 1


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
    fields = ['feedback']


class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    model = Feedback
    fields = ['feedback']
    template_name_suffix = '_form'
