# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-08 04:33
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('grad_year', models.IntegerField()),
                ('degree', models.CharField(choices=[('H', 'High school'), ('P', 'P U'), ('M', 'Masters'), ('B', 'Bachelors')], max_length=100)),
                ('field_of_study', models.CharField(max_length=100)),
                ('score', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
                ('url', models.URLField(null=True)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='jobposting',
            name='link',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='jobposting',
            name='organization',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='jobposting',
            name='stipend',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='jobposting',
            name='type',
            field=models.CharField(choices=[('I', 'Internship'), ('F', 'Full Time')], default='F', max_length=1),
        ),
        migrations.AlterField(
            model_name='personal',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '9999999999'.", regex='^[0-9]{10}$')]),
        ),
        migrations.AlterField(
            model_name='personorganization',
            name='organization',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.AddField(
            model_name='project',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Personal'),
        ),
        migrations.AddField(
            model_name='education',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Personal'),
        ),
    ]
