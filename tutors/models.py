from django.db import models
from collections import Iterable


from quiz.models import Quizzes

def deep_flatten(field):
    """
    Get items from nested Iterable

    :param Iterable field:
    :return Generator:
    """
    for item in field:
        if isinstance(item, Iterable):
            for x in deep_flatten(item):
                yield x
        else:
            yield item


class CategoryQuestion(models.Model):
    name = models.CharField(max_length=100, null=False)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL,
                                        null=True, blank=True,
                                        db_column='parent_id',
                                        related_name='childrens')

    def __str__(self):
        return f'{self.name}'

    @property
    def childrens_pk_list(self):
        return list(deep_flatten(self._get_childrens_pk()))

    def _get_childrens_pk(self):
        """
        Build a family of CategoryQuestion tree

        :return List:
        """
        children = self.childrens.all()

        if not children:
            return [self.pk]

        return [self.pk, [obj._get_childrens_pk() for obj in children]]

    class Meta:
        db_table = "Categories_questions"


class Question(models.Model):
    quiz = models.ManyToManyField(Quizzes)
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
                                 db_column='question_id')
    answer_text = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f'{self.question.question_text}: {self.answer_text}'

    class Meta:
        db_table = "Answers"
