import datetime
import json
import operator

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, ListView

from groups.models import Shedule
from quiz.models import Results
from tutors.models import Questions
from .forms import QuestionSaveForm

__all__ = ['TestPlayer', 'StartTest', ]


class StartTest(PermissionRequiredMixin, ListView):
    """
    Return a list of all available tests
    get_queryset: return queryset of Quizzes model objects
    """
    template_name = 'test_player/start_test.html'
    context_object_name = 'quizzes'
    _not_started_quizzes = None
    permission_required = 'quiz.view_test_player'

    def get_queryset(self):
        """Takes list of all Quizzes for Group of user, that are actual now
        and shows only those that will end the last """
        quizzes = Shedule.objects.filter(
            group__user=self.request.user, end__gt=timezone.now()). \
            order_by('quiz_id', 'begin').distinct('quiz_id')
        self._not_started_quizzes = quizzes.filter(begin__gt=timezone.now())
        result = sorted(quizzes, key=operator.attrgetter('end'))
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_started'] = self._not_started_quizzes
        return context


class TestPlayer(UserPassesTestMixin, FormView):
    """
    View which render form with test questions one by one
    """
    template_name = 'test_player/test_player.html'
    form_class = QuestionSaveForm
    permission_required = 'quiz.view_results'

    def get_success_url(self):
        """
        Handling user activity while passing the test

        """

        if 'next_to' in self.request.POST or 'prev' in self.request.POST:
            return self._handle_previous_and_next_questions()
        if 'submit_finish' in self.request.POST:
            return reverse_lazy('quiz:result-list',
                                kwargs={'user_id': self.request.session[
                                    '_auth_user_id']})
        return reverse_lazy('test_player:test_player',
                            kwargs={'quiz_id': self.kwargs[
                                'quiz_id'], 'question_number':
                                        self.request.POST.get('next')})

    def get_context_data(self, **kwargs):
        """
        :param self
        :param kwargs: form kwargs such as \
         self.kwargs['quiz_id'], self.kwargs['question_number'];
        :var current_quiz(int): id current test(form keyword argument) \
         for accessing to session data about current test;
        :var question_number(int): number current question \
         (form keyword argument);
        :return: context object for template which will be rendered that view

        """
        context = super().get_context_data(**kwargs)
        current_quiz = self.kwargs['quiz_id']
        question_number = self.kwargs['question_number']

        context['questions'] = Questions.objects.filter(
            quiz_id=current_quiz).order_by('question_number')

        context['current_question'] = get_object_or_404(
            Questions, quiz_id=current_quiz,
            question_number=question_number)

        context['quiz_id'] = current_quiz

        self._handle_finish_test(context)

        return context

    def get_form_kwargs(self):
        """
        :param self
        :var current_quiz(int): id current test(form keyword argument) \
         for accessing to session data about current test;
        :var question_number(int): number current question \
         (form keyword argument);
        :var current_question(model object): single model object \
         of current question;
        :var current_answers(queryset): model queryset object with answers \
         related with current question;
        :return additional form instance attributes

        """
        kwargs = super().get_form_kwargs()
        current_quiz = self.kwargs['quiz_id']
        question_number = self.kwargs['question_number']

        current_question = get_object_or_404(
            Questions, quiz_id=current_quiz,
            question_number=question_number)
        current_answers = current_question.answers_set.all()

        if current_quiz in self.request.session and question_number in \
                self.request.session[current_quiz].keys():
            default_answer = self.request.session[current_quiz].get(
                question_number)
        else:
            default_answer = None

        return dict(kwargs, answers=current_answers,
                    default_choice=default_answer)

    def form_valid(self, form):
        """
        :param self
        :param form
        :var current_quiz(int): id current test(form keyword argument) \
         for accessing to session data about current test;
        :var question_number(int): number current question \
         (form keyword argument);
        :var answer(int): selected answer for current question
        :var session_user(int): current logged in user who passes test
        :var initial_question(int): question which will be rendered first
        :return form_valid(form)

        """
        current_quiz = self.kwargs['quiz_id']
        question_number = self.kwargs['question_number']
        answer = form.cleaned_data.get('answers')
        session_user = self.request.session['_auth_user_id']
        initial_question = dict.fromkeys(list(zip(*Questions.objects.filter(
            quiz=current_quiz).values_list(
            'question_number').order_by('question_number')))[0], None)

        # initialize session variable for test and setting initial values \
        # (nested dictionary like: {quiz_id: {question_number: answer}}

        if self.request.session.setdefault(current_quiz, False):
            session_data = self.request.session[current_quiz]
        else:
            session_data = initial_question
            self.request.session[current_quiz] = session_data

        # updating session data with relevant data
        if answer:
            session_data.update({
                question_number: answer})
        self.request.session[current_quiz] = session_data

        # handling submit modal button, and saving to database
        if 'submit_finish' in self.request.POST:
            timezone.now()
            date = datetime.datetime.now()
            result = []
            # checking that the user answered all the questions, \
            # because it`s important condition for \
            # correct calculation of the result
            for key in self.request.session[current_quiz]:
                if self.request.session[current_quiz].get(key) is None:
                    messages.info(self.request,
                                  "You need to answer all the questions!!!")
                    return super(TestPlayer, self).form_invalid(form)
                result.append(
                    int(self.request.session[current_quiz].get(key)))
            result = json.dumps(result, ensure_ascii=False)
            # saving user replies to a database for \
            # further calculation by formula
            Results.objects.create(user_id=int(session_user),
                                   quiz_id=int(current_quiz),
                                   pass_date=date,
                                   result=result)
            del self.request.session[
                current_quiz]  # clear session data about passed and saved test

        return super(TestPlayer, self).form_valid(form)

    def _handle_finish_test(self, context):
        """
        :param self
        :param context: 'context' object which is being rendered that view;
        :var self.current_quiz(int): id current test(form keyword argument) \
         for accessing to session data about current test;
        :var self.session(dict): with session data from session object;
        :var self.answers(list): with dict values which contain user answers;
        :var self.answered(int): counter, which represent \
         answered answers (not None).
        :var number_of_questions(int): number of questions \
         related with current quiz

        """
        current_quiz = self.kwargs['quiz_id']
        number_of_questions = Questions.objects.filter(
            quiz=current_quiz).count()
        self.session = dict(self.request.session)

        if current_quiz in self.session.keys():
            self.answers = self.session[current_quiz].values()

            self.answered = sum(1 for answer in self.answers if answer)

            if self.answered >= (number_of_questions - 1):
                context['is_can_be_finished'] = True

    def _handle_previous_and_next_questions(self):
        """
        :param self
        :var self.current_quiz(int): id current test(form keyword argument) \
         for accessing to session data about current test;
        :var self.question_number(int): number current question \
         (form keyword argument)
        :var self.question_count(int): total quantity of questions in the test
        :return: reverse to next or previous question with \
         form kwargs: id of test, number of question that will be rendered

        """
        self.current_quiz = self.kwargs['quiz_id']
        self.question_number = self.kwargs['question_number']
        self.question_count = Questions.objects.filter(
            quiz_id=self.current_quiz).count()

        next_question_number = int(self.question_number) + 1
        prev_question_number = int(self.question_number) - 1

        if 'next_to' in self.request.POST \
                and next_question_number <= self.question_count:

            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': self.current_quiz,
                                        'question_number': next_question_number
                                        })
        elif 'prev' in self.request.POST and prev_question_number > 0:

            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': self.current_quiz,
                                        'question_number': prev_question_number
                                        })
        else:
            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': self.current_quiz,
                                        'question_number': self.question_number
                                        })

    def test_func(self):
        a = Shedule.objects.filter(group__user=self.request.user). \
            filter(end__gt=datetime.datetime.now()). \
            filter(begin__lte=datetime.datetime.now()). \
            filter(quiz=self.kwargs['quiz_id'])
        return a.exists()
