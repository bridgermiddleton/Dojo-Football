# Generated by Django 2.2.6 on 2019-10-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.ForeignKey(on_delete='CASCADE', related_name='players', to='football_app.User'),
        ),
        migrations.AlterField(
            model_name='tweek',
            name='user',
            field=models.ForeignKey(on_delete='CASCADE', related_name='weeks', to='football_app.User'),
        ),
    ]
