# Generated by Django 2.1.5 on 2019-01-27 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
        ('tutors', '0010_merge_20190126_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(to='quiz.Quizzes'),
        ),
    ]