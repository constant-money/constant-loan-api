# Generated by Django 2.1.4 on 2019-01-28 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_auto_20190128_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanprogram',
            name='max_term',
            field=models.IntegerField(default=6),
        ),
        migrations.AddField(
            model_name='loanprogram',
            name='min_term',
            field=models.IntegerField(default=6),
        ),
    ]
