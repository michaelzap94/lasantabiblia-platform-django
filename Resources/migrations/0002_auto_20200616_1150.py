# Generated by Django 3.0.6 on 2020-06-16 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='size',
            field=models.IntegerField(default=0),
        ),
    ]
