# Generated by Django 3.0.1 on 2020-09-29 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20200927_1839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='complete',
            new_name='private',
        ),
    ]
