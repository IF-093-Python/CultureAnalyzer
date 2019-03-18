import datetime
import json
import operator

from django.contrib import messages
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (FormView, ListView)

from groups.models import Shedule
from quiz.models import Results
from tutors.models import Questions
from .forms import QuestionSaveForm

__all__ = ['StartTest', 'TestPlayer', ]


class StartTest(PermissionRequiredMixin, ListView):
    """
    Return a list of all available tests

    get_queryset: return queryset of Quizzes model objects

    """
    template_name = 'test_player/start_test.html'
    context_object_name = 'quizzes'
    __not_started_quizzes = None
    permission_required = 'quiz.view_test_player'

    def get_queryset(self):
        """
        Takes list of all Quizzes for Group of user, that are actual now
        and shows only those that will end the last

         """
        quizzes = Shedule.objects.filter(group__user=self.request.user). \
            filter(end__gt=timezone.now()). \
            order_by('quiz_id', 'begin').distinct('quiz_id')
        self._not_started_quizzes = quizzes.filter(begin__gt=timezone.now())
        # we can't sort result by begin and then by end so we make it like this
        result = sorted(quizzes, key=operator.attrgetter('end'))
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_started'] = self._not_started_quizzes
        return context


class TestPlayer(UserPassesTestMixin, FormView):
    """
    View which render form with test questions one by one
    """
    template_name = 'test_player/test_player.html'
    form_class = QuestionSaveForm
    permission_required = 'quiz.view_test_player'

    def get_success_url(self):
        """
        Handling user activity, while passing the test

        :var next_number(int): number of question, which has been selected \
         by user;

        """
        current_quiz, _ = self.get_quiz_data()
        next_number = int(self.request.POST.get('next_number'))
        success_url = reverse_lazy('test_player:test_player',
                                   kwargs={'quiz_id': current_quiz,
                                           'question_number': next_number})
        if 'prev' in self.request.POST:
            success_url = self._handle_previous_question()
        elif 'next_to' in self.request.POST:
            success_url = self._handle_next_question()
        elif 'submit_finish' in self.request.POST:
            success_url = self._handle_finish_test()
        return success_url

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
        current_quiz, question_number = self.get_quiz_data()
        questions = Questions.objects.filter(
            quiz_id=current_quiz).order_by('question_number')
        current_question = questions.get(question_number=question_number)
        context['questions'] = questions
        context['current_question'] = current_question
        context['quiz_id'] = current_quiz

        self._count_user_answers(context)

        return context

    def get_quiz_data(self):
        """
        :param self
        :var current_quiz(int): id current test(form keyword argument) \
         for accessing to session data about current test;
        :var question_number(int): number current question \
         (form keyword argument);
        :returns data about test from form keyword arguments.

        """
        current_quiz = self.kwargs['quiz_id']
        question_number = self.kwargs['question_number']
        return current_quiz, question_number

    def get_form_kwargs(self):
        """
        :param self
        :var current_answers(queryset): model queryset object with answers \
         related with current question;
        :return additional form instance attributes;

        """
        kwargs = super().get_form_kwargs()
        current_quiz, question_number = self.get_quiz_data()
        current_question = get_object_or_404(Questions,
                                             quiz_id=current_quiz,
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
        :param form
        :var answer(int): selected answer for current question
        :return form_valid(form).

        """
        current_quiz, question_number = self.get_quiz_data()
        answer = form.cleaned_data.get('answers')
        # checking if session variable exist, if not - call method, which \
        # set default initial values (used only once during the first request)
        if current_quiz not in self.request.session:
            self._setting_initial_session_data()

        # updating session data with relevant data
        session_data = self.request.session[current_quiz]
        if answer:
            session_data.update(
                {question_number: answer}
            )
        self.request.session[current_quiz] = session_data

        return super(TestPlayer, self).form_valid(form)

    def _setting_initial_session_data(self):
        """
        Method, which set default initial values (used only once \
        during the first request).

        :var questions(queryset object): which contain ordered questions \
         numbers;
        :var initial_questions(dict): which contain initial values \
         for questions.

        """
        current_quiz, question_number = self.get_quiz_data()

        questions = Questions.objects.filter(quiz=current_quiz).values_list(
            'question_number', flat=True).order_by('question_number')
        initial_questions = dict.fromkeys(questions)

        self.request.session.setdefault(current_quiz, None)
        self.request.session[current_quiz] = initial_questions

    def _saving_user_answers(self):
        """
        Method, which save user answers to database such as json object.

        :var session_data(dict): with session data from session object;
        :var session_user(int): current logged in user who passes test.

        """
        current_quiz, _ = self.get_quiz_data()
        session_user = self.request.session['_auth_user_id']
        session_data = dict(self.request.session[current_quiz])
        result = []

        for answer in session_data:
            result.append(int(session_data.get(answer)))
        result = json.dumps(result, ensure_ascii=False)

        Results.objects.create(user_id=int(session_user),
                               quiz_id=int(current_quiz),
                               pass_date=datetime.datetime.now(
                                   timezone.get_current_timezone()),
                               result=result)
        del self.request.session[current_quiz]

    def _count_user_answers(self, context):
        """
        Method, which count answered questions, initialize context variable \
         which uses for display finish button.

        :param context: 'context' object which is being rendered that view;
        :var number_of_questions(int): number of questions \
         related with current quiz;
        :var answers(list): with dict values which contain user answers;
        :var answered(int): counter, which represent \
         answered answers (not None);
        :var context variable, which uses in template for display finish button

        """
        current_quiz, _ = self.get_quiz_data()
        number_of_questions = Questions.objects.filter(
            quiz=current_quiz).count()

        if current_quiz in self.request.session.keys():
            answers = dict(self.request.session[current_quiz]).values()

            answered = sum(1 for answer in answers if answer)

            if answered >= (number_of_questions - 1):
                context['is_can_be_finished'] = True

    def _handle_previous_question(self):
        """
        Method, which handles click action for button "previous question".

        :var prev_question_number(int): number of previous question which \
         ought to be rendered such as next one;
        :return: reverse to previous question with \
         form kwargs: id of test and number of question that will be rendered.

        """
        current_quiz, question_number = self.get_quiz_data()
        prev_question_number = int(question_number) - 1

        if prev_question_number > 0:
            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': current_quiz,
                                        'question_number': prev_question_number
                                        })

    def _handle_next_question(self):
        """
        Method, which handles click action for button "next question".

        :var next_question_number(int): number of next question which ought \
         to be rendered such as next one;
        :var question_count(int): total quantity of questions in the test;
        :return: reverse to next question with \
         form kwargs: id of test, number of question that will be rendered.

         """
        current_quiz, question_number = self.get_quiz_data()
        question_count = Questions.objects.filter(
            quiz_id=current_quiz).count()
        next_question_number = int(question_number) + 1

        if next_question_number <= question_count:
            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': current_quiz,
                                        'question_number': next_question_number
                                        })

    def _handle_finish_test(self):
        """
        Method, which handles click action for button "Submit(test)".

        :return: reverse to not answered question with \
         form keyword arguments: id of test, number of not answered question.

        """
        current_quiz, _ = self.get_quiz_data()

        for question in self.request.session[current_quiz]:
            if self.request.session[current_quiz].get(question) is None:
                messages.info(self.request,
                              "You need to answer all the questions!!!")
                return reverse('test_player:test_player',
                               kwargs={'quiz_id': current_quiz,
                                       'question_number': question})
        self._saving_user_answers()

        return reverse('quiz:result-list', kwargs={
            'user_id': self.request.session['_auth_user_id']})

    @transaction.atomic()
    def test_func(self):
        date_time = datetime.datetime.now(timezone.get_current_timezone())
        quiz_exist = Shedule.objects.filter(group__user=self.request.user,
                                            end__gt=date_time,
                                            begin__lte=date_time,
                                            quiz=self.kwargs[
                                                'quiz_id']).exists()
        return quiz_exist
