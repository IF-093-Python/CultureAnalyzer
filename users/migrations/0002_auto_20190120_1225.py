# Generated by Django 2.1.5 on 2019-01-20 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(db_column='role_id', default=3, on_delete=django.db.models.deletion.PROTECT, to='users.Role'),
        ),
    ]