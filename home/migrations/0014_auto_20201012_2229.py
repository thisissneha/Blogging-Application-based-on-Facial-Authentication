# Generated by Django 3.0.1 on 2020-10-12 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20201012_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verifyemail',
            old_name='user',
            new_name='customer',
        ),
    ]
