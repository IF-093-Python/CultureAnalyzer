from django.contrib import admin
from .models import CategoryQuestion, Question, Answer

admin.site.register(CategoryQuestion)
admin.site.register(Question)
admin.site.register(Answer)
# Register your models here.
