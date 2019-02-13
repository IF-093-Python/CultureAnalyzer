from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from CultureAnalyzer.settings.default import ITEMS_ON_PAGE

from .forms import QuestionCreateForm, AnswerCreateForm
from .models import Questions, Answers

__all__ = ['QuestionListView', 'CreateQuestionView', 'UpdateQuestionView',
           'DeleteQuestionView', 'AnswerListView', 'CreateAnswerView',
           'UpdateAnswerView', 'DeleteAnswerView', ]


def get_min_missing_value(model, filter_id):
    """
    Function looks for the least missed value of the number to the question
    in the test among the created questions.
    :return: minimum missing value
    """
    list_of_number = get_numbers(model, filter_id)
    if not list_of_number:
        return 1
    max_value = int(max(list_of_number[0]))
    for value in range(1, max_value + 1):
        if value not in list_of_number[0]:
            return value
    return max_value + 1


def get_numbers(model, filter_id):
    """
    :return: values from column 'question_number'/ 'answer_number' as a
    tuple of values.
    """
    if model == 'Questions':
        return list(zip(*Questions.objects.filter(quiz=filter_id).values_list(
            'question_number').order_by('question_number')))
    return list(zip(*Answers.objects.filter(question=filter_id).values_list(
        'answer_number').order_by('answer_number')))


class QuestionListView(LoginRequiredMixin, ListView):
    model = Questions
    template_name = 'tutors/questions_list.html'
    context_object_name = 'questions'
    paginate_by = ITEMS_ON_PAGE

    def get_queryset(self):
        """
        The search for questions is based on fields 'question_number' or
        'question_text'.
        Returns the queryset of questions that you want to display.
        """
        questions = Questions.objects.all().annotate(
            num_answer=Count('answers')).order_by('quiz', 'question_number')
        question_search = self.request.GET.get("question_search")
        if question_search:
            return questions.filter(
                Q(question_text__icontains=question_search) | Q(
                    question_number__icontains=question_search))
        return questions

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Returns context data for displaying the list of questions.
        """
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("question_search")
        return context


class CreateQuestionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Questions
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('tutors:questions_list')
    success_message = 'Question "№%(number)d" was created successfully!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           number=self.object.question_number)

    def form_valid(self, form):
        form.instance.question_number = get_min_missing_value('Questions',
                                                              form.
                                                              cleaned_data.get(
                                                                  'quiz'))
        return super(CreateQuestionView, self).form_valid(form)


class UpdateQuestionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Questions
    form_class = QuestionCreateForm
    template_name = 'tutors/question_create.html'
    success_url = reverse_lazy('tutors:questions_list')
    success_message = 'Question "№%(number)d" was updated successfully!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           number=self.object.question_number)


class DeleteQuestionView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Questions
    template_name = 'tutors/question_delete.html'
    success_url = reverse_lazy('tutors:questions_list')
    success_message = 'Question: "%(question_number)s" was deleted ' \
                      'successfully!'

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
        context['q'] = self.request.GET.get("answer_search")
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
        context['q'] = get_object_or_404(Questions,
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
        context['q'] = get_object_or_404(Questions,
                                         pk=self.kwargs['question_id'])
        return context


class DeleteAnswerView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Answers
    template_name = 'tutors/answer_delete.html'
    success_message = 'Answers: "%(answer_text)s" was deleted successfully!'

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
