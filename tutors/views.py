from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
# from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import CategoryQuestion, Question, Answer
from .forms import CategoryCreateForm, QuestionCreateForm, AnswerCreateForm


# from quiz.models import  Quizzes


class CategoryListView(LoginRequiredMixin, ListView):
    model = CategoryQuestion
    template_name = 'tutors/categories_list.html'
    context_object_name = 'categories'


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = CategoryQuestion
    form_class = CategoryCreateForm
    template_name = 'tutors/category_create.html'
    success_url = reverse_lazy('tutors:categories_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super().form_valid(form)


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = CategoryQuestion
    form_class = CategoryCreateForm
    template_name = 'tutors/category_create.html'
    success_url = reverse_lazy('tutors:categories_list')

    def get_success_url(self):
        return reverse_lazy('tutors:categories_list')

    def get_form_kwargs(self):  # defined in ModelFormMixin class
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(UpdateCategoryView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = CategoryQuestion
    template_name = 'tutors/category_delete.html'
    success_url = reverse_lazy('tutors:categories_list')


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'tutors/questions_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(category_question=get_object_or_404(
            CategoryQuestion, pk=self.kwargs['category_id']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            CategoryQuestion, pk=self.kwargs['category_id'])
        return context


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'

    def get_success_url(self):
        return reverse_lazy('tutors:questions_list', kwargs={
            'category_id': self.object.category_question.id
        })

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.category_question = get_object_or_404(
            CategoryQuestion, pk=self.kwargs['category_id'])
        obj.save()
        return super().form_valid(form)


class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'

    def get_success_url(self):
        return reverse_lazy('tutors:questions_list', kwargs={
            'category_id': self.kwargs['category_id']
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'tutors/question_delete.html'

    def get_success_url(self):
        return reverse_lazy('tutors:questions_list', kwargs={'category_id':
                                                                 self.object.category_question.id
                                                             })


class AnswerListView(LoginRequiredMixin, ListView):
    model = Answer
    template_name = 'tutors/answers_list.html'
    context_object_name = 'answers'

    def get_queryset(self):
        return Answer.objects.filter(question=get_object_or_404(
            Question, pk=self.kwargs['question_id']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(
            Question, pk=self.kwargs['question_id'])
        return context


class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list', kwargs={
            'question_id': self.kwargs['question_id']
        })

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.question = get_object_or_404(
            Question, pk=self.kwargs['question_id'])
        obj.save()
        return super().form_valid(form)


class UpdateAnswerView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list', kwargs={
            'question_id': self.kwargs['question_id']
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteAnswerView(LoginRequiredMixin, DeleteView):
    model = Answer
    template_name = 'tutors/answer_delete.html'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list', kwargs={'question_id':
                                                               self.object.question.id
                                                           })
