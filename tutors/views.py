from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from CultureAnalyzer.settings.default import ITEMS_ON_PAGE

from quiz.models import Quizzes

from .forms import QuestionCreateForm, AnswerCreateForm
from .models import Questions, Answers
from .service import get_min_missing_value

__all__ = ['CreateQuestionView', 'UpdateQuestionView',
           'DeleteQuestionView', 'AnswerListView', 'CreateAnswerView',
           'UpdateAnswerView', 'DeleteAnswerView', ]


class CreateQuestionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Questions
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_message = 'Question "#%(number)d" was created successfully!'

    def get_success_url(self):
        return reverse_lazy('quiz:detail-quiz', kwargs={'pk': self.kwargs[
            'quiz_id']})

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           number=self.object.question_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = get_object_or_404(Quizzes, pk=self.kwargs['quiz_id'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Questions(question_number=get_min_missing_value(
            'Questions', self.kwargs['quiz_id']), quiz=Quizzes(
                self.kwargs['quiz_id']))
        return kwargs


class UpdateQuestionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Questions
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_message = 'Question "№%(number)d" was updated successfully!'

    def get_success_url(self):
        return reverse_lazy('quiz:detail-quiz', kwargs={'pk': self.kwargs[
            'quiz_id']})

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           number=self.object.question_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = get_object_or_404(Quizzes, pk=self.kwargs['quiz_id'])
        return context


class DeleteQuestionView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Questions
    template_name = 'tutors/question_delete.html'
    success_message = 'Question: "%(question_number)s" was deleted ' \
                      'successfully!'

    def get_success_url(self):
        return reverse_lazy('quiz:detail-quiz', kwargs={'pk': self.kwargs[
            'quiz_id']})

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        """
        Returns context data about success deleted question in message.
        """
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


class AnswerListView(LoginRequiredMixin, ListView):
    model = Answers
    template_name = 'tutors/answers_list.html'
    context_object_name = 'answers'
    paginate_by = ITEMS_ON_PAGE

    def get_queryset(self):
        answers = Answers.objects.filter(
            question=self.kwargs['question_id']).order_by('answer_number')
        answer_search = self.request.GET.get("answer_search")
        if answer_search:
            return answers.filter(answer_text__icontains=answer_search)
        return answers

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Questions,
                                                pk=self.kwargs['question_id'])
        context['search'] = self.request.GET.get("answer_search")
        return context


class CreateAnswerView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Answers
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'
    success_message = 'Answers: "%(answer_text)s" was created successfully!'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list',
                            kwargs={'question_id': self.kwargs['question_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Questions,
                                                pk=self.kwargs['question_id'])
        return context

    def get_form_kwargs(self):
        """
        Function initializes the value of the foreign key
        """
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Answers(answer_number=get_min_missing_value(
            'Answers', self.kwargs['question_id']), question=Questions(
                self.kwargs['question_id']))
        return kwargs


class UpdateAnswerView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Answers
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'
    success_message = 'Answers: "%(answer_text)s" was updated successfully!'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list',
                            kwargs={'question_id': self.kwargs['question_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Questions, pk=self.kwargs[
            'question_id'])
        return context


class DeleteAnswerView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Answers
    template_name = 'tutors/answer_delete.html'
    success_message = 'Answers: "%(answer_text)s" was deleted successfully!'

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        """
        Returns context data about success deleted answer in message.
        """
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list',
                            kwargs={'question_id': self.object.question.id})
