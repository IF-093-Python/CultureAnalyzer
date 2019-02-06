# Generated by Django 2.1.5 on 2019-02-04 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190130_2333'),
        ('tutors', '0009_auto_20190125_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.IntegerField()),
                ('question_text', models.TextField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quizzes')),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='categoryquestion',
            name='parent_category',
        ),
        migrations.RemoveField(
            model_name='question',
            name='category_question',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='CategoryQuestion',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.Questions'),
        ),
        migrations.AlterUniqueTogether(
            name='questions',
            unique_together={('quiz', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='answers',
            unique_together={('question', 'answer_text')},
        ),
    ]
