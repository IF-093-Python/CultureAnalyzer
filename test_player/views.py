from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
from .forms import QuestionSaveForm
from quiz.models import Quizzes
from tutors.models import Questions, Answers


def index(request):
    return render(request, 'test_player/quizz.html')


class TestPlayer(FormView):
    template_name = 'test_player/test_player.html'
    form_class = QuestionSaveForm

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
        return dict(kwargs, answers=current_answers)


