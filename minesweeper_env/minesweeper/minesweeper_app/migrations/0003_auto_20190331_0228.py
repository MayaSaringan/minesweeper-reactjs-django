# Generated by Django 2.1.7 on 2019-03-31 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper_app', '0002_auto_20190331_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
