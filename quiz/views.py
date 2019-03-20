from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views import generic

from CultureAnalyzer.settings.default import ITEMS_ON_PAGE

from quiz.forms import QuizCreateForm
from quiz.models import Quizzes
from tutors.models import Questions


class QuizzesList(LoginRequiredMixin, generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    template_name = 'quiz/quizzes_list.html'
    paginate_by = 2

    def get_queryset(self):
        quizzes = Quizzes.objects.all().order_by('title')
        quiz_search = self.request.GET.get("quiz_search")
        if quiz_search:
            return quizzes.filter(
                Q(title__icontains=quiz_search))
        return quizzes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuizzesList, self).get_context_data(**kwargs)
        context['search'] = self.request.GET.get("quiz_search")
        return context


class CreateQuizView(LoginRequiredMixin, generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quiz:quizzes-list')


class QuizDetailView(LoginRequiredMixin, generic.ListView):
    model = Questions
    context_object_name = 'questions'
    template_name = 'quiz/quiz_detail.html'
    paginate_by = ITEMS_ON_PAGE

    def get_queryset(self):
        """
        The search for questions is based on fields 'question_text'.
        Returns the queryset of questions that you want to display.
        """
        questions = Questions.objects.filter(quiz=self.kwargs['pk']).annotate(
            num_answer=Count('answers')).order_by('question_number')
        question_search = self.request.GET.get("question_search")
        if question_search:
            return questions.filter(
                Q(question_text__icontains=question_search))
        return questions

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get("question_search")
        context['quiz'] = get_object_or_404(Quizzes, pk=self.kwargs['pk'])
        return context


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
