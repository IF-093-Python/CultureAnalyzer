from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db import models
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Questions, Answers
from .forms import QuestionCreateForm, AnswerCreateForm
from quiz.models import  Quizzes

ITEMS_PER_PAGE = 5


class QuestionListView(LoginRequiredMixin, ListView):
    model = Questions
    template_name = 'tutors/questions_list.html'
    context_object_name = 'questions'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """
        Returns the queryset of categories that you want to display.
        """
        questions = Questions.objects.all().annotate(
            num_answer=Count('answers')).order_by('pk')
        q = self.request.GET.get("question_search")
        if q:
            return questions.filter(question__icontains=q, title__icontains=q)
        return questions

    def get_context_data(self, **kwargs):
        """
        Returns context data for displaying the list of categories.
        """
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("question_search")
        return context


class CreateQuestionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Questions
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('tutors:questions_list')
    success_message = 'Question: "%(title)s" was created successfully'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super().form_valid(form)


class UpdateQuestionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Questions
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('tutors:questions_list')
    success_message = 'Question: "%(title)s" was updated successfully'

    def get_success_url(self):
        return reverse_lazy('tutors:questions_list')

    def get_form_kwargs(self):  # defined in ModelFormMixin class
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(UpdateQuestionView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class DeleteQuestionView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Questions
    template_name = 'tutors/question_delete.html'
    success_url = reverse_lazy('tutors:questions_list')
    success_message = 'Question: "%(title)s" was deleted successfully'

    def delete(self, request, *args, **kwargs):
        """
        Returns context data about success deleted category in message.
        """
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


class AnswerListView(LoginRequiredMixin, ListView):
    model = Answers
    template_name = 'tutors/answers_list.html'
    context_object_name = 'answers'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        answers = Answers.objects.filter(question=get_object_or_404(
            Questions, pk=self.kwargs['question_id'])).order_by('pk')
        q = self.request.GET.get("answer_search")
        if q:
            return answers.filter(answer_text__icontains=q)
        return answers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(
            Questions, pk=self.kwargs['question_id'])
        context['q'] = self.request.GET.get("answer_search")
        return context


class CreateAnswerView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Answers
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'
    success_message = 'Answers: "%(answer_text)s" was created successfully'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list',
                            kwargs={'question_id': self.kwargs['question_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = get_object_or_404(Questions,
                                         pk=self.kwargs['question_id'])
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.question = get_object_or_404(Questions, pk=self.kwargs[
            'question_id'])
        obj.save()
        return super().form_valid(form)


class UpdateAnswerView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Answers
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'
    success_message = 'Answers: "%(answer_text)s" was updated successfully'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list',
                            kwargs={'question_id': self.kwargs['question_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = get_object_or_404(Questions,
                                         pk=self.kwargs['question_id'])
        return context


class DeleteAnswerView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Answers
    template_name = 'tutors/answer_delete.html'
    success_message = 'Answers: "%(answer_text)s" was deleted successfully'

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
