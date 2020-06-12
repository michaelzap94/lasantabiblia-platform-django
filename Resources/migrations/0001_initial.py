# Generated by Django 3.0.6 on 2020-06-12 00:40

import Resources.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('language', models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('pt', 'Portuguese'), ('fr', 'French'), ('ko', 'Korean'), ('ru', 'Russian')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('resource_type', models.CharField(choices=[('bibles', 'Bible'), ('concordances', 'Concordance'), ('dictionaries', 'Dictionary'), ('maps', 'Map')], max_length=50)),
                ('version', models.IntegerField(default=0)),
                ('resource', models.FileField(upload_to=Resources.models.Resource.makeResourcePath)),
                ('is_published', models.BooleanField(default=True)),
                ('list_date', models.DateTimeField(auto_now=True)),
                ('size', models.DecimalField(blank=True, decimal_places=1, max_digits=10)),
                ('filename', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
