import ast
import json
from collections import ChainMap

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.db.models import Q
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from quiz.forms import QuizCreateForm
from quiz.models import Quizzes, Results
from quiz.service import get_final_result
from indicators.models import CountryIndicator
from feedbacks.models import Feedback, Recommendation


class QuizzesList(LoginRequiredMixin, generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    ordering = ('title')
    template_name = 'quiz/quizzes_list.html'
    __search = False

    def get_queryset(self):
        result = super(QuizzesList, self).get_queryset()
        if self.request.GET.get('data_search'):
            result = result.filter(
                title__contains=self.request.GET.get('data_search'))
            self.__search = True
        elif self.request.GET.get('clear'):
            self.__search = False
            return redirect('quiz:quizzes-list')
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuizzesList, self).get_context_data(**kwargs)
        context['search'] = self.__search
        return context


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
        context['result'] = list(get_final_result(self.request.user.profile,
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
