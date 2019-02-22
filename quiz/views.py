import ast
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from CultureAnalyzer.settings import ITEMS_ON_PAGE
from feedbacks.models import Feedback
from indicators.models import CountryIndicator
from quiz.forms import QuizCreateForm
from quiz.models import Quizzes, Results
from quiz.service import get_final_result
from tutors.models import Questions


class QuizzesList(LoginRequiredMixin, generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    ordering = ('title')
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

    def get_context_data(self, **kwargs):
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


class ResultsListView(LoginRequiredMixin, generic.ListView):
    model = Results
    template_name = 'quiz/result_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        results = Results.objects.filter(user=self.request.user)
        return results


class CurrentResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'quiz/column_chart_from_result.html'

    def post(self, request, **kwargs):
        context = self.get_context_data()
        countries_values = {}
        countries_names = []
        countries_feedbacks = {}
        if self.request.method == 'POST' and self.request.POST.getlist(
                'select_indicator'):
            options = self.request.POST.getlist('select_indicator')
            for o in options:
                countries_values.update(ast.literal_eval(o))
                indicator_obj = context['country_indicators'].get(
                    iso_code=list(ast.literal_eval(o))[0])
                countries_names.append(indicator_obj.name)
                countries_feedbacks[indicator_obj.name] = get_feedback(
                    list(ast.literal_eval(o).values())[0], context['result'])

        context['countries_values'] = countries_values
        context['countries_names'] = countries_names
        context['countries_feedbacks'] = countries_feedbacks
        return super(CurrentResultView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = list(get_final_result(self.request.user,
                                                  self.kwargs['pk']).values())
        context['country_indicators'] = CountryIndicator.objects.all()
        context['countries_values'] = {}
        context['countries_feedbacks'] = {}
        return context


def get_feedback(indicator_obj, dict_result):
    indicator_name = ['pdi', 'idv', 'mas', 'uai', 'lto', 'ivr']
    indicators_feedbacks = {}
    for val in range(6):
        indicators_difference = abs(indicator_obj[val] - dict_result[val])
        indicator_feedback = Feedback.objects.filter(
            Q(min_value__lte=indicators_difference) &
            Q(max_value__gte=indicators_difference),
            indicator__iexact=indicator_name[val])
        indicators_feedbacks[indicator_name[val]] = indicator_feedback
    return indicators_feedbacks
