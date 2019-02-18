import json

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import CASCADE

TYPE_OF_QUIZ = (('Business', 'Business'), ('General', 'General'))


class Quizzes(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    type_of_quiz = models.CharField(choices=TYPE_OF_QUIZ, max_length=20)

    def __str__(self):
        return self.title


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=CASCADE, null=False)
    pass_date = models.DateTimeField(null=False)
    result = JSONField()

    def __str__(self):
        return self.user.username

    @property
    def get_score(self):
        """get list of dictionaries from JSON, which contains user answers"""
        self.score = json.loads(self.result)
        return self.score

    @property
    def calculate_index(self, *args):
        """
            The index formula is(example for PDI): index = 35(m07 – m02) + /
            25(m20 – m23)
            in which m07 is the mean score for question 07, etc.
        """

        index = args[1] * (args[2] - args[3]) + args[4] * (args[5] - args[6])
        return index

    @property
    def get_pdi(self):
        """pdi is mean the Power Distance Index (PDI)"""
        pdi = self.calculate_index(35,
                                   self.score[6]["a_num"],
                                   self.score[1]["a_num"],
                                   25,
                                   self.score[19]["a_num"],
                                   self.score[22]["a_num"])
        return pdi

    @property
    def get_idv(self):
        """idv is mean Individualism Index (IDV)"""
        idv = self.calculate_index(35,
                                   self.score[3]["a_num"],
                                   self.score[0]["a_num"],
                                   35,
                                   self.score[8]["a_num"],
                                   self.score[5]["a_num"])
        return idv

    @property
    def get_mas(self):
        """mas is mean Masculinity Index (MAS)"""
        mas = self.calculate_index(35,
                                   self.score[4]["a_num"],
                                   self.score[2]["a_num"],
                                   35,
                                   self.score[7]["a_num"],
                                   self.score[9]["a_num"])
        return mas

    @property
    def get_uai(self):
        """uai is mean Uncertainty Avoidance Index (UAI)"""
        uai = self.calculate_index(45,
                                   self.score[17]["a_num"],
                                   self.score[15]["a_num"],
                                   25,
                                   self.score[20]["a_num"],
                                   self.score[23]["a_num"])
        return uai

    @property
    def get_lto(self):
        """lto is mean Long Term Orientation Index (LTO)"""
        lto = self.calculate_index(45,
                                   self.score[12]["a_num"],
                                   self.score[13]["a_num"],
                                   25,
                                   self.score[18]["a_num"],
                                   self.score[21]["a_num"])
        return lto

    @property
    def get_ivr(self):
        """ivr is mean Indulgence versus Restraint Index (IVR)"""
        ivr = self.calculate_index(35,
                                   self.score[11]["a_num"],
                                   self.score[10]["a_num"],
                                   40,
                                   self.score[16]["a_num"],
                                   self.score[15]["a_num"])
        return ivr
