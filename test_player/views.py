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
                                'quiz_id'], 'question_title':
                                self.request.POST.get('next')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Questions.objects.filter(
            quiz_id=self.kwargs['quiz_id']).order_by('title')
        context['current_question'] = get_object_or_404(Questions,
                                                        quiz_id=self.kwargs[
                                                            'quiz_id'],
                                                        title=self.kwargs[
                                                            'question_title'])

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        current_questions = get_object_or_404(Questions,
                                              quiz_id=self.kwargs['quiz_id'],
                                              title=self.kwargs[
                                                  'question_title'])
        current_answers = current_questions.answers_set.all()
        if self.kwargs['question_title'] in self.request.session.keys():
            d_answer = self.request.session[self.kwargs['question_title']]
        else:
            d_answer = ''
        return dict(kwargs, answers=current_answers, default_choice=d_answer)

    def form_valid(self, form):
        self.request.session[self.kwargs['question_title']] = \
            form.cleaned_data.get('answers')
        print(self.request.session.items())
        return super(TestPlayer, self).form_valid(form)

