from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from quiz.forms import QuizCreateForm
from quiz.models import Quizzes


class QuizzesList(LoginRequiredMixin, generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    ordering = ('title',)
    template_name = 'quiz/quizzes_list.html'

    def get_queryset(self):
        result = super(QuizzesList, self).get_queryset()
        if self.request.GET.get('data_search'):
            result = result.filter(
                title__contains=self.request.GET.get('data_search'))
        elif self.request.GET.get('clear'):
            return redirect('quiz:quizzes-list')
        return result


class CreateQuizView(LoginRequiredMixin, generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quiz:quizzes-list')


class DeleteQuizView(LoginRequiredMixin, generic.DeleteView):
    model = Quizzes
    context_object_name = 'quiz'
    template_name = 'quiz/quiz_delete.html'
    success_url = reverse_lazy('quiz:quizzes-list')


class UpdateQuizView(LoginRequiredMixin, generic.UpdateView):
    model = Quizzes
    form_class = QuizCreateForm
    template_name = 'quiz/quiz_update.html'
    success_url = reverse_lazy('quiz:quizzes-list')
