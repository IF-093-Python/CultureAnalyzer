from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, \
    DetailView, UpdateView
from .models import Question, Answer
from .forms import QuestionCreateForm, AnswerCreateForm


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


class DetailQuestionView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'tutors/question_detail.html'
    context_object_name = 'question'


class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('question_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'tutors/question_delete.html'
    success_url = reverse_lazy('question_list')
