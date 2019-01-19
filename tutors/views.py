from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from .models import Question
from .forms import QuestionCreateForm


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'tutors/question_list.html'
    context_object_name = 'questions'


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        # obj.quiz = self.quiz.quiz_id
        obj.save()
        return super().form_valid(form)


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'tutors/question_delete.html'
    success_url = reverse_lazy('question_list')
