# Generated by Django 2.1.5 on 2019-02-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0003_auto_20190213_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='type_of_quiz',
            field=models.CharField(
                choices=[('Business', 'Business'), ('General', 'General')],
                max_length=20),
        ),
    ]
