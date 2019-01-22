from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import CategoryQuestion, Question, Answer
from .forms import CategoryCreateForm, QuestionCreateForm, AnswerCreateForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = CategoryQuestion
    template_name = 'tutors/categories_list.html'
    context_object_name = 'categories'


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = CategoryQuestion
    form_class = CategoryCreateForm
    template_name = 'tutors/category_create.html'
    success_url = reverse_lazy('categories_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super().form_valid(form)


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'tutors/question_list.html'
    context_object_name = 'questions'


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.category_question = get_object_or_404(CategoryQuestion, pk=self.kwargs['category_id'])
        obj.save()
        return super().form_valid(form)


class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('question_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'tutors/question_delete.html'
    success_url = reverse_lazy('question_list')


class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'
    success_url = reverse_lazy('answer_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.question = get_object_or_404(Question, pk=self.kwargs[
                                                            'question_id'])
        obj.save()
        return super().form_valid(form)
