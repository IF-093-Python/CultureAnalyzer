import datetime
import json
import operator

from django.contrib import messages
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (FormView, ListView)

from groups.models import Shedule
from quiz.models import Results
from test_player.forms import QuestionSaveForm
from tutors.models import Questions

__all__ = ['StartTest', 'TestPlayer', ]


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
        """
        Takes list of all Quizzes for Group of user, that are actual now
        and shows only those that will end the last

         """
        quizzes = Shedule.objects.filter(group__user=self.request.user,
                                         end__gt=timezone.now()). \
            order_by('quiz_id', 'start').distinct('quiz_id')
        self._not_started_quizzes = quizzes.filter(start__gt=timezone.now())
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
        Handling user activity, while passing the test.

        :var next_number(int): number of question, which has been selected
         by user;
        :return success_url
        """
        current_quiz, _ = self.get_quiz_data()
        next_number = self.request.POST.get('next_number')
        success_url = reverse_lazy('test_player:test_player',
                                   kwargs={'quiz_id': current_quiz,
                                           'question_number': next_number})
        if 'prev' in self.request.POST:
            success_url = self._handle_previous_question()
        elif 'next_to' in self.request.POST:
            success_url = self._handle_next_question()
        elif 'submit_finish' in self.request.POST:
            success_url = self._handle_finish_test(current_quiz)
        return success_url

    def get_context_data(self, **kwargs):
        """
        :param kwargs: form kwargs such as self.kwargs['quiz_id'],
         self.kwargs['question_number'];
        :var current_quiz(int): id current test(form keyword argument) for
         accessing to session data about current test;
        :var question_number(int): number of current question
         (form keyword argument);
        :return: context object for template which will be rendered that view

        """

        context = super().get_context_data(**kwargs)
        current_quiz, question_number = self.get_quiz_data()
        questions = Questions.objects.filter(
            quiz_id=current_quiz).order_by('question_number')
        current_question = questions.get(question_number=question_number)
        context.update({'questions': questions,
                        'current_question': current_question,
                        'quiz_id': current_quiz})
        self._count_user_answers(current_quiz, context)

        return context

    def get_quiz_data(self):
        """
        Method which get id of current test and number of current question from
         form keyword arguments and return them for further use
          in other methods.
        :var current_quiz(int): id current test(form keyword argument) for
         accessing to session data about current test;
        :var question_number(int): number current question
         (form keyword argument);
        :returns data about test from form keyword arguments.

        """
        current_quiz = self.kwargs['quiz_id']
        question_number = self.kwargs['question_number']
        return current_quiz, question_number

    def get_initial(self):
        """
        Method, which uses for updating form instance "initial" argument with
         default choice if it was previously selected.
        :var default_answer(int): default answer which ought to be added
         such as initial choice in form;
        :return: dict with updated initial values.

        """
        initial = super(TestPlayer, self).get_initial()
        current_quiz, question_number = self.get_quiz_data()

        if current_quiz in self.request.session and question_number in \
                self.request.session[current_quiz].keys():
            default_answer = self.request.session.get(current_quiz).get(
                question_number)
        else:
            default_answer = None

        initial.update({'default_choice': default_answer})

        return initial

    def get_form_kwargs(self):
        """
        Method, which uses for updating form instance keyword arguments with
         answers related with current question;

        :var current_question(object): single object of question by lookup
         parameters from form keyword arguments such as quiz_id,
         question_number;
        :var current_answers(queryset): queryset object with answers related
         with current question;
        :return: kwargs(dict): with updated form instance keyword arguments.

        """
        kwargs = super(TestPlayer, self).get_form_kwargs()
        current_quiz, question_number = self.get_quiz_data()
        current_question = Questions.objects.get(
            quiz=current_quiz,
            question_number=question_number)
        current_answers = current_question.answers_set.all()

        kwargs.update({'answers': current_answers})

        return kwargs

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

        # updating session with relevant data
        session_data = self.request.session[current_quiz]
        if form.has_changed():
            session_data.update(
                {question_number: answer}
            )
        self.request.session[current_quiz] = session_data

        return super(TestPlayer, self).form_valid(form)

    def _setting_initial_session_data(self):
        """
        Method, which set default initial values (used only once during the
         first request).

        :var questions(queryset object): which contain ordered questions
         numbers;
        :var initial_questions(dict): which contain initial key(questions),
         values(answers) for questions.

        """
        current_quiz, _ = self.get_quiz_data()

        questions = Questions.objects.filter(quiz=current_quiz).values_list(
            'question_number', flat=True).order_by('question_number')
        initial_questions = dict.fromkeys(questions)

        self.request.session.setdefault(current_quiz, None)
        self.request.session[current_quiz] = initial_questions

    def _saving_user_answers(self, current_quiz):
        """
        Method, which save user answers to database such as json object.

        :var session_data(dict): with session data from session object;
        :var session_user(int): current logged in user who passes test.

        """
        session_user = self.request.session['_auth_user_id']
        session_data = self.request.session[current_quiz]
        result = []

        for answer in session_data:
            result.append(int(session_data.get(answer)))
        result = json.dumps(result, ensure_ascii=False)

        Results.objects.create(user_id=int(session_user),
                               quiz_id=int(current_quiz),
                               pass_date=datetime.datetime.now(
                                   timezone.get_current_timezone()),
                               result=result)
        self.request.session.pop(current_quiz, None)

    def _count_user_answers(self, current_quiz, context):
        """
        Method, which count answered questions, initialize context variable
         which uses for display finish button.

        :param context: 'context' object which is being rendered that view;
        :var number_of_questions(int): number of questions related with current
         quiz;
        :var answers(list): with dict values which contain user answers;
        :var answered(int): counter, which represent answered answers
         (not None);
        :var context['is_can_be_finished']: variable, which uses in template
         for displaying finish button.

        """
        number_of_questions = Questions.objects.filter(
            quiz=current_quiz).count()

        if current_quiz in self.request.session.keys():
            answers = self.request.session[current_quiz].values()

            answered = sum(1 for answer in answers if answer)

            if answered >= (number_of_questions - 1):
                context.update({'is_can_be_finished': True})

    def _handle_previous_question(self):
        """
        Method, which handles click action for button "previous question".

        :var prev_question_number(int): number of previous question which
         ought to be rendered such as next one;
        :return: reverse to previous question with form kwargs: id of test
         and number of question that will be rendered.

        """
        current_quiz, question_number = self.get_quiz_data()
        prev_question_number = int(question_number) - 1

        if prev_question_number > 0:
            success_url = reverse_lazy(
                'test_player:test_player',
                kwargs={'quiz_id': current_quiz,
                        'question_number': prev_question_number
                        })
        else:
            success_url = reverse_lazy(
                'test_player:test_player',
                kwargs={'quiz_id': current_quiz,
                        'question_number': question_number
                        })
        return success_url

    def _handle_next_question(self):
        """
        Method, which handles click action for button "next question".

        :var next_question_number(int): number of next question which ought to
         be rendered such as next one;
        :var question_count(int): total quantity of questions in the test;
        :return: reverse to next question with form kwargs: id of test and
         number of question that will be rendered.

         """
        current_quiz, question_number = self.get_quiz_data()
        question_count = Questions.objects.filter(
            quiz_id=current_quiz).count()
        next_question_number = int(question_number) + 1

        if next_question_number <= question_count:
            success_url = reverse_lazy(
                'test_player:test_player',
                kwargs={'quiz_id': current_quiz,
                        'question_number': next_question_number
                        })
        else:
            success_url = reverse_lazy(
                'test_player:test_player',
                kwargs={'quiz_id': current_quiz,
                        'question_number': question_number
                        })
        return success_url

    def _handle_finish_test(self, current_quiz):
        """
        Method, which handles click action for button "Submit(test)".

        :return: success_url, reverse to not answered question with
         form keyword arguments: id of test, number of not answered question.

        """
        for question in self.request.session[current_quiz]:
            if self.request.session[current_quiz].get(question) is None:
                messages.info(self.request,
                              "You need to answer all the questions!!!")
                success_url = reverse('test_player:test_player',
                                      kwargs={'quiz_id': current_quiz,
                                              'question_number': question})
                return success_url
        self._saving_user_answers(current_quiz)

        return reverse('quiz:result-list', kwargs={'pk': self.request.user.id})

    @transaction.atomic()
    def test_func(self):
        """

        :return: boolean value which mean quiz existing
        """
        date_time = datetime.datetime.now(timezone.get_current_timezone())
        quiz_id, _ = self.get_quiz_data()
        quiz_exist = Shedule.objects.filter(group__user=self.request.user,
                                            end__gt=date_time,
                                            start__lte=date_time,
                                            quiz=quiz_id).exists()
        return quiz_exist
