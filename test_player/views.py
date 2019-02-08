from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import QuestionSaveForm
from quiz.models import Quizzes
from tutors.models import Questions, Answers


def index(request):
    return render(request, 'test_player/quizz.html')


class TestPlayer(FormView):
    template_name = 'test_player/test_player.html'
    form_class = QuestionSaveForm

    def get_success_url(self):
        return reverse_lazy('test_player:detail',
                            kwargs={'quiz_id': self.kwargs[
                                'quiz_id'], 'question_number':
                                        self.request.POST.get('next')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Questions.objects.filter(
            quiz_id=self.kwargs['quiz_id']).order_by('question_number')
        context['current_question'] = get_object_or_404(Questions,
                                                        quiz_id=self.kwargs[
                                                            'quiz_id'],
                                                        question_number=
                                                        self.kwargs[
                                                            'question_number'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        current_questions = get_object_or_404(Questions,
                                              quiz_id=self.kwargs['quiz_id'],
                                              question_number=self.kwargs[
                                                  'question_number'])
        current_answers = current_questions.answers_set.all()
        if self.kwargs['quiz_id'] in self.request.session and self.kwargs[
            'question_number'] in self.request.session[self.kwargs[
            'quiz_id']].keys():
            d_answer = self.request.session[self.kwargs['quiz_id']].get(self.kwargs[
                        'question_number'])
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
        s.update({
            self.kwargs['question_number']: form.cleaned_data.get(
                'answers')})
        self.request.session[self.kwargs['quiz_id']] = s
        print(self.request.session.items())
        return super(TestPlayer, self).form_valid(form)
