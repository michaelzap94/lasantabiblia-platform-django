# Generated by Django 3.0.6 on 2020-06-18 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestAPIS', '0003_auto_20200618_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verses_learned',
            name='state',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='verses_marked',
            name='state',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
