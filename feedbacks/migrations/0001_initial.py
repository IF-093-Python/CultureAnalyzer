# Generated by Django 2.1.5 on 2019-01-21 19:33

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
            ],
            options={
                'db_table': 'Feedbacks',
            },
        ),
    ]
