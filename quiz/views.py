from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from quiz.forms import QuizCreateForm
from quiz.models import Quizzes


class QuizzesList(LoginRequiredMixin, PermissionRequiredMixin,
                  generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    ordering = ('title',)
    template_name = 'quiz/quizzes_list.html'
    permission_required = 'quiz.view_quizzes'

    def get_queryset(self):
        result = super(QuizzesList, self).get_queryset()
        if self.request.GET.get('data_search'):
            result = result.filter(
                title__contains=self.request.GET.get('data_search'))
        elif self.request.GET.get('clear'):
            return redirect('quiz:quizzes-list')
        return result


class CreateQuizView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quiz:quizzes-list')
    permission_required = 'quiz.add_quizzes'


class DeleteQuizView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.DeleteView):
    model = Quizzes
    context_object_name = 'quiz'
    template_name = 'quiz/quiz_delete.html'
    success_url = reverse_lazy('quiz:quizzes-list')
    permission_required = 'quiz.delete_quizzes'


class UpdateQuizView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.UpdateView):
    model = Quizzes
    form_class = QuizCreateForm
    template_name = 'quiz/quiz_update.html'
    success_url = reverse_lazy('quiz:quizzes-list')
    permission_required = 'quiz.change_quizzes'
