# Generated by Django 3.0.1 on 2020-10-01 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_auto_20200930_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='slug',
        ),
        migrations.AddField(
            model_name='task',
            name='post_id',
            field=models.AutoField(default='70', primary_key=True, serialize=False),
        ),
    ]
