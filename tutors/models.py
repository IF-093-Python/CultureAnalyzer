from django.db import models
# from quiz.models import Quizzes


class CategoryQuestion(models.Model):
    name = models.CharField(max_length=100, null=False)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL,
                                        null=True, blank=True,
                                        db_column='parent_id')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "Categories_questions"


class Question(models.Model):
    # quiz = models.ManyToManyField(Quizzes)
    question_text = models.CharField(max_length=100, null=False)
    category_question = models.ForeignKey(CategoryQuestion,
                                          on_delete=models.CASCADE,
                                          null=True, blank=True,
                                          db_column='category_id')

    def __str__(self):
        return f'{self.question_text}'

    class Meta:
        db_table = "Questions"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 db_column='answer_id')
    answer_text = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f'{self.question.question_text}: {self.answer_text}'

    class Meta:
        db_table = "Answers"
