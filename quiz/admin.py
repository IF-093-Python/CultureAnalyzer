from django.contrib import admin
from quiz.models import Quizzes, Results
from django.contrib.auth.models import Permission

admin.site.register(Quizzes)
admin.site.register(Results)
admin.site.register(Permission)