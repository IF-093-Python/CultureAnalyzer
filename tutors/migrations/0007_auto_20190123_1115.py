# Generated by Django 2.1.5 on 2019-01-23 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0006_auto_20190123_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='question_answer',
            new_name='question',
        ),
    ]
