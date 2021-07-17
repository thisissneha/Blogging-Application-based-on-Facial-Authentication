# Generated by Django 3.0.1 on 2020-10-10 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Category',
            field=models.CharField(choices=[('food', 'FOOD'), ('technical', 'TECHNICAL'), ('technology', 'TECHNOLOGY'), ('news', 'NEWS'), ('movies', 'MOVIES'), ('history', 'HISTORY'), ('knowledge', 'KNOWLEDGE'), ('fitness', 'FITNESS'), ('games', 'GAMES'), ('social', 'SOCIAL'), ('economy', 'ECONOMY'), ('business', 'BUSINESS'), ('others', 'OTHERS')], default='select', max_length=11),
        ),
    ]
