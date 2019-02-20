import ast
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# Create your views here.
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views import generic

from CultureAnalyzer.settings.default import ITEMS_ON_PAGE

from quiz.forms import QuizCreateForm
from quiz.models import Quizzes, Results
from tutors.models import Questions
from quiz.service import get_final_result
from indicators.models import CountryIndicator
from feedbacks.models import Feedback, Recommendation


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


@login_required()
def get_result_from(request, pk):
    dict_result = get_final_result(request.user.profile, pk)
    result = list(dict_result.values())
    country_indicators = CountryIndicator.objects.all()
    countries_values = {}
    countries_feedbacks = {}
    if request.method == 'POST' and request.POST.getlist('select_indicator'):
        options = request.POST.getlist('select_indicator')
        countries_names = []
        for o in options:
            o = o.split(':')
            countries_values[o[0]] = list(map(int, o[1].split()))
            indicator_obj = country_indicators.get(iso_code=o[0])
            countries_names.append(indicator_obj.name)
            countries_feedbacks[indicator_obj.name] = get_feedback(
                indicator_obj, dict_result)
        context = {
            'result': result,
            'country_indicators': country_indicators,
            'countries_values': countries_values,
            'dict_result': dict_result,
            'countries_names': countries_names,
            'countries_feedbacks': countries_feedbacks,
        }
    else:
        context = {
            'result': result,
            'country_indicators': country_indicators,
            'countries_values': countries_values,
            'dict_result': dict_result,
            }
    return render(request, 'quiz/column_chart_from_result.html', context)


def get_feedback(indicator_obj, dict_result):
    indicators_feedbacks = {}
    for ind, val in dict_result.items():
        indicators_difference = abs(getattr(indicator_obj, ind) - val)
        indicator_feedback = Feedback.objects.filter(
                            Q(min_value__lte=indicators_difference) &
                            Q(max_value__gte=indicators_difference),
                            indicator__iexact=ind)
        indicators_feedbacks[ind] = indicator_feedback
    return indicators_feedbacks
