# Generated by Django 2.1.7 on 2019-03-31 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper_app', '0005_auto_20190331_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='square',
            name='xcoord',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='square',
            name='ycoord',
            field=models.IntegerField(default=0),
        ),
    ]
