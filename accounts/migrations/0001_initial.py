# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 14:48
from __future__ import unicode_literals

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
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=100)),
                ('startdateedu', models.CharField(max_length=100)),
                ('enddateedu', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='signupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dateofbirth', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('skills', models.TextField(null=True)),
                ('interests', models.TextField(null=True)),
                ('objectivestatement', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='workexperienceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('startDate', models.CharField(max_length=100)),
                ('endDate', models.CharField(max_length=100)),
                ('UserExperience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.signupModel')),
            ],
        ),
        migrations.AddField(
            model_name='education',
            name='UserEducation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.signupModel'),
        ),
    ]
