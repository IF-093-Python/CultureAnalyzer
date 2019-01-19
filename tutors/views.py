from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .models import Question
from .forms import QuestionCreateForm


@login_required
class QuestionListView(ListView):
    model = Question
    template_name = 'tutors/question_list.html'
    context_object_name = 'questions'


@login_required
class CreateQuestionView(CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        # obj.quiz = self.quiz.quiz_id
        obj.save()
        return super().form_valid(form)


@login_required
class DeleteQuestionView(DeleteView):
    model = Question
    template_name = 'tutors/question_delete.html'
    success_url = reverse_lazy('question_list')

