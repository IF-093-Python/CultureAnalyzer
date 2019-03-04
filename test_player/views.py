import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, ListView

from quiz.models import Results, Quizzes
from tutors.models import Questions
from users.models import CustomUser
from .forms import QuestionSaveForm

__all__ = ['TestPlayer', 'TestStart', ]


class TestStart(PermissionRequiredMixin, ListView):
    template_name = 'test_player/start_test.html'
    context_object_name = 'quizzes'
    permission_required = 'quiz.view_results'

    def get_queryset(self):
        quizzes = Quizzes.objects.all()
        return quizzes


class TestPlayer(PermissionRequiredMixin, FormView):
    template_name = 'test_player/test_player.html'
    form_class = QuestionSaveForm
    permission_required = 'quiz.view_results'

    def get_success_url(self):
        if 'next_to' in self.request.POST or 'prev' in self.request.POST:
            return self._handle_previous_and_next_questions()
        if 'finish' in self.request.POST:
            return reverse_lazy('quiz:result-list',
                                kwargs={'user_id': self.request.session[
                                    '_auth_user_id']})
        return reverse_lazy('test_player:test_player',
                            kwargs={'quiz_id': self.kwargs[
                                'quiz_id'], 'question_number':
                                         self.request.POST.get('next')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Questions.objects.filter(
            quiz_id=self.kwargs['quiz_id']).order_by('question_number')
        context['current_question'] = get_object_or_404(
            Questions, quiz_id=self.kwargs['quiz_id'],
            question_number=self.kwargs['question_number'])
        context['quiz_id'] = self.kwargs['quiz_id']
        self._handle_finish_test(context)

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        current_questions = get_object_or_404(
            Questions, quiz_id=self.kwargs['quiz_id'],
            question_number=self.kwargs['question_number'])
        current_answers = current_questions.answers_set.all()
        if self.kwargs['quiz_id'] in self.request.session and self.kwargs[
            'question_number'] in self.request.session[
            self.kwargs['quiz_id']].keys():
            d_answer = self.request.session[self.kwargs['quiz_id']].get(
                self.kwargs['question_number'])
        else:
            d_answer = None
        return dict(kwargs, answers=current_answers, default_choice=d_answer)

    def form_valid(self, form):
        if self.request.session.setdefault(self.kwargs['quiz_id'], False):
            s = self.request.session[self.kwargs['quiz_id']]
        else:
            s = dict.fromkeys(list(zip(*Questions.objects.filter(
                quiz=self.kwargs['quiz_id']).values_list(
                'question_number').order_by('question_number')))[0], None)
            self.request.session[self.kwargs['quiz_id']] = s

        if form.cleaned_data.get('answers'):
            s.update({
                self.kwargs['question_number']: form.cleaned_data.get(
                    'answers')})
        self.request.session[self.kwargs['quiz_id']] = s
        print(s)
        if 'finish' in self.request.POST:
            quiz_id = self.kwargs['quiz_id']
            user = CustomUser.objects.get(
                pk=self.request.session['_auth_user_id'])
            quiz = Quizzes.objects.get(pk=quiz_id)
            timezone.now()
            date = datetime.datetime.now()
            result = []
            for key in self.request.session[quiz_id]:
                if self.request.session[quiz_id].get(key) is None:
                    messages.info(self.request,
                                  "You need to answer all the questions!!!")
                    return super(TestPlayer, self).form_invalid(form)

                result.append(int(self.request.session[quiz_id].get(key)))
            result = json.dumps(result, ensure_ascii=False)
            Results.objects.create(user=user, quiz=quiz,
                                   pass_date=date,
                                   result=result)
            del self.request.session[self.kwargs[
                'quiz_id']]  # clear session data about passed and saved test

        return super(TestPlayer, self).form_valid(form)

    def _handle_finish_test(self, context):
        session = dict(self.request.session)
        if self.kwargs['quiz_id'] in session.keys():
            answers = self.request.session[
                self.kwargs['quiz_id']].values()
            answered = sum(1 for answer in answers if answer)
            if answered >= 23:
                context['is_can_be_finished'] = True

    def _handle_previous_and_next_questions(self):
        question_count = Questions.objects.filter(
            quiz_id=self.kwargs['quiz_id']).count()
        next_question_number = int(self.kwargs['question_number']) + 1
        prev_question_number = int(self.kwargs['question_number']) - 1

        if 'next_to' in self.request.POST \
                and next_question_number <= question_count:
            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': self.kwargs[
                                    'quiz_id'], 'question_number':
                                            next_question_number
                                        })
        elif 'prev' in self.request.POST and prev_question_number > 0:
            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': self.kwargs[
                                    'quiz_id'], 'question_number':
                                            prev_question_number
                                        })
        else:
            return reverse_lazy('test_player:test_player',
                                kwargs={'quiz_id': self.kwargs[
                                    'quiz_id'], 'question_number':
                                            self.kwargs['question_number']
                                        })
