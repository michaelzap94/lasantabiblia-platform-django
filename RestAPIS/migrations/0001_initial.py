# Generated by Django 3.0.6 on 2020-06-18 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Verses_Marked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('label_id', models.IntegerField()),
                ('book_number', models.IntegerField()),
                ('chapter', models.IntegerField()),
                ('verseFrom', models.IntegerField()),
                ('verseTo', models.IntegerField()),
                ('label_name', models.CharField(max_length=200)),
                ('label_color', models.CharField(max_length=200)),
                ('label_permanent', models.IntegerField(default=0)),
                ('note', models.TextField(blank=True)),
                ('date_created', models.CharField(max_length=200)),
                ('date_updated', models.CharField(max_length=200)),
                ('UUID', models.CharField(max_length=100)),
                ('state', models.IntegerField(blank=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Verses_Learned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('UUID', models.CharField(max_length=100)),
                ('label_id', models.IntegerField()),
                ('learned', models.IntegerField(default=0)),
                ('priority', models.IntegerField(default=0)),
                ('state', models.IntegerField(blank=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=10)),
                ('permanent', models.IntegerField(default=0)),
                ('state', models.IntegerField(blank=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
