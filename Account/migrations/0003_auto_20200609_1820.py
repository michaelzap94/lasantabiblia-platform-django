# Generated by Django 3.0.6 on 2020-06-09 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_auto_20200609_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='firstname',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='fullname',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='lastname',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]