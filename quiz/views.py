import ast
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from indicators.models import CountryIndicator
from quiz.forms import QuizCreateForm
from quiz.models import Quizzes, Results
from quiz.service import get_final_result


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

    def get_queryset(self, **kwargs):
        results = Results.objects.filter(user=self.request.user)
        print(self.request.user)
        return results


class ResultsView(TemplateView):

    def get_context_data(self, **kwargs):
        result = list(get_final_result(self.request.user.profile,
                                       self.kwargs['pk']).values())
        country_indicators = CountryIndicator.objects.all()
        countries_values = []

        # context = super(ResultsView, self).get_context_data(**kwargs)
        context = {
            'result': result,
            'country_indicators': country_indicators,
            'countries_values': countries_values,
        }
        return context

    def post(self):
        if self.request.method == 'POST' and self.request.POST.getlist(
                'select_indicator'):
            options = self.request.POST.getlist('select_indicator')
            countries_values = json.loads(options)
            print(countries_values)
            context = {
                'result': result,
                'country_indicators': country_indicators,
                'countries_values': countries_values,
            }


def get_result_from(request, pk):
    result = list(get_final_result(request.user.profile, pk).values())
    print(result)
    country_indicators = CountryIndicator.objects.all()

    countries_values = []
    if request.method == 'POST' and request.POST.getlist('select_indicator'):
        options = request.POST.getlist('select_indicator')
        # print(type(options))
        countries_values = ast.literal_eval(options[0])
        print(countries_values)
        context = {
            'result': result,
            'country_indicators': country_indicators,
            'countries_values': countries_values,
        }
    else:
        context = {
            'result': result,
            'country_indicators': country_indicators,
            'countries_values': countries_values,
        }
    return render(request, 'quiz/column_chart_from_result.html', context)
