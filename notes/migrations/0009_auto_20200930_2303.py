# Generated by Django 3.0.1 on 2020-09-30 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_remove_task_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='slug',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
    ]