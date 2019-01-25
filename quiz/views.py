from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from quiz.models import *
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin, PermissionDenied
from quiz.forms import QuizCreateForm


class QuizzesList(LoginRequiredMixin, generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    ordering = ('title')
    template_name = 'quiz/quizzes_list.html'

    def get_queryset(self):
        result = super(QuizzesList, self).get_queryset()
        if self.request.GET.get('data_search'):
            result = result.filter(
                title__contains=self.request.GET.get('data_search'))
        return result


class CreateQuizView(LoginRequiredMixin, generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quiz:quizzes-list')

    def user_gains_perms(request):
        user_id =
        user = get_object_or_404(User,)
        # any permission check will cache the current set of permissions
        if user.has_perm('quiz.create_quiz'):
            return redirect('quiz:create-quiz')
        else:
            raise PermissionDenied



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
