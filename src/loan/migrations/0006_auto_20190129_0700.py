# Generated by Django 2.1.4 on 2019-01-29 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0005_auto_20190129_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmember',
            name='user_name',
            field=models.CharField(default='NoName', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='loanmemberapplication',
            unique_together={('application', 'member')},
        ),
    ]
