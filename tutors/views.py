from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from .forms import CategoryCreateForm, QuestionCreateForm, AnswerCreateForm
from .models import CategoryQuestion, Question, Answer

ITEMS_PER_PAGE = 5


class CategoryListView(LoginRequiredMixin, ListView):
    model = CategoryQuestion
    template_name = 'tutors/categories_list.html'
    context_object_name = 'categories'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """
        Returns the queryset of categories that you want to display.
        """
        categories = CategoryQuestion.objects.all().annotate(
            num_question=Count('question')).order_by('pk')
        q = self.request.GET.get("category_search")
        if q:
            return categories.filter(name__icontains=q)
        return categories

    def get_context_data(self, **kwargs):
        """
        Returns context data for displaying the list of categories.
        """
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("category_search")
        return context


class CreateCategoryView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CategoryQuestion
    form_class = CategoryCreateForm
    template_name = 'tutors/category_create.html'
    success_url = reverse_lazy('tutors:categories_list')
    success_message = 'Category: "%(name)s" was created successfully'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super().form_valid(form)


class UpdateCategoryView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CategoryQuestion
    form_class = CategoryCreateForm
    template_name = 'tutors/category_create.html'
    success_url = reverse_lazy('tutors:categories_list')
    success_message = 'Category: "%(name)s" was updated successfully'

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


class DeleteCategoryView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CategoryQuestion
    template_name = 'tutors/category_delete.html'
    success_url = reverse_lazy('tutors:categories_list')
    success_message = 'Category: "%(name)s" was deleted successfully'

    def delete(self, request, *args, **kwargs):
        """
        Returns context data about success deleted category in message.
        """
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'tutors/questions_list.html'
    context_object_name = 'questions'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """
        Returns the queryset of question from some category that you want to
        display.
        """
        questions = Question.objects.filter(
            category_question=get_object_or_404(CategoryQuestion,
                                                pk=self.kwargs[
                                                    'category_id'])).annotate(
            num_answer=Count('answer')).order_by('pk')
        q = self.request.GET.get("question_search")
        if q:
            return questions.filter(question_text__icontains=q)
        return questions

    def get_context_data(self, **kwargs):
        """
        Returns context data for displaying the list of questions and the
        list of subcategories rom some category.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            CategoryQuestion, pk=self.kwargs['category_id'])
        context['children'] = CategoryQuestion.objects.filter(
            parent_category=get_object_or_404(CategoryQuestion,
                                              pk=self.kwargs[
                                                  'category_id'])).annotate(
            num_question=Count('question')).order_by('pk')
        context['q'] = self.request.GET.get("question_search")
        return context


class CreateQuestionView(LoginRequiredMixin, PermissionRequiredMixin,
                         SuccessMessageMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_message = 'Question: "%(question_text)s" was created successfully'
    permission_required = 'tutors.add_questions'

    def get_success_url(self):
        return reverse_lazy('tutors:questions_list', kwargs={
            'category_id': self.object.category_question.id
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['c'] = get_object_or_404(CategoryQuestion,
                                         pk=self.kwargs['category_id'])
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.category_question = get_object_or_404(CategoryQuestion,
                                                            pk=self.kwargs[
                                                                'category_id'])
        obj.save()
        return super().form_valid(form)


class UpdateQuestionView(LoginRequiredMixin, PermissionRequiredMixin,
                         SuccessMessageMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_message = 'Question: "%(question_text)s" was updated successfully'
    permission_required = 'tutors.change_questions'

    def get_success_url(self):
        return reverse_lazy('tutors:questions_list', kwargs={
            'category_id': self.kwargs['category_id']
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['c'] = get_object_or_404(CategoryQuestion,
                                         pk=self.kwargs['category_id'])
        return context


class DeleteQuestionView(LoginRequiredMixin, PermissionRequiredMixin,
                         SuccessMessageMixin, DeleteView):
    model = Question
    template_name = 'tutors/question_delete.html'
    success_message = 'Question: "%(question_text)s" was deleted successfully'
    permission_required = 'tutors.delete_questions'

    def delete(self, request, *args, **kwargs):
        """
        Returns context data about success deleted question in message.
        """
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('tutors:questions_list', kwargs={
            'category_id': self.object.category_question.id
            })


class AnswerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Answer
    template_name = 'tutors/answers_list.html'
    context_object_name = 'answers'
    paginate_by = ITEMS_PER_PAGE
    permission_required = 'tutors.view_answers'

    def get_queryset(self):
        answers = Answer.objects.filter(question=get_object_or_404(
            Question, pk=self.kwargs['question_id'])).order_by('pk')
        q = self.request.GET.get("answer_search")
        if q:
            return answers.filter(answer_text__icontains=q)
        return answers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(
            Question, pk=self.kwargs['question_id'])
        context['q'] = self.request.GET.get("answer_search")
        return context


class CreateAnswerView(LoginRequiredMixin, PermissionRequiredMixin,
                       SuccessMessageMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'
    success_message = 'Answers: "%(answer_text)s" was created successfully'
    permission_required = 'tutors.add_answers'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list',
                            kwargs={'question_id': self.kwargs['question_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = get_object_or_404(Question,
                                         pk=self.kwargs['question_id'])
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.question = get_object_or_404(Question, pk=self.kwargs[
            'question_id'])
        obj.save()
        return super().form_valid(form)


class UpdateAnswerView(LoginRequiredMixin, PermissionRequiredMixin,
                       SuccessMessageMixin, UpdateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'tutors/answer_create.html'
    success_message = 'Answers: "%(answer_text)s" was updated successfully'
    permission_required = 'tutors.change_answers'

    def get_success_url(self):
        return reverse_lazy('tutors:answers_list',
                            kwargs={'question_id': self.kwargs['question_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = get_object_or_404(Question,
                                         pk=self.kwargs['question_id'])
        return context


class DeleteAnswerView(LoginRequiredMixin, PermissionRequiredMixin,
                       SuccessMessageMixin, DeleteView):
    model = Answer
    template_name = 'tutors/answer_delete.html'
    success_message = 'Answers: "%(answer_text)s" was deleted successfully'
    permission_required = 'tutors.delete_answers'

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
