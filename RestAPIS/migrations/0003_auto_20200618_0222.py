# Generated by Django 3.0.6 on 2020-06-18 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestAPIS', '0002_auto_20200618_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verses_learned',
            name='priority',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='verses_marked',
            name='label_permanent',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]