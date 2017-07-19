# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 13:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import journal.models


class Migration(migrations.Migration):

    replaces = [('journal', '0001_initial'), ('journal', '0002_journalentry_module'), ('journal', '0003_imageentry'), ('journal', '0004_journalentry_posted'), ('journal', '0005_runentry'), ('journal', '0006_auto_20170616_2145'), ('journal', '0007_auto_20170616_2326'), ('journal', '0008_auto_20170717_1133'), ('journal', '0009_auto_20170717_1249')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('produced', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='NoteEntry',
            fields=[
                ('journalentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='journal.JournalEntry')),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'note entries',
            },
            bases=('journal.journalentry',),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='module',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='journal.Module'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ImageEntry',
            fields=[
                ('journalentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='journal.JournalEntry')),
                ('image', models.ImageField(upload_to=journal.models.module_upload_path)),
            ],
            options={
                'verbose_name_plural': 'image entries',
            },
            bases=('journal.journalentry',),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='RunEntry',
            fields=[
                ('journalentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='journal.JournalEntry')),
                ('runnumber', models.IntegerField()),
                ('eventcount', models.BigIntegerField()),
                ('recorded', models.DateTimeField()),
                ('data', models.FileField(upload_to=journal.models.module_upload_path)),
            ],
            bases=('journal.journalentry',),
        ),
        migrations.CreateModel(
            name='OutputImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=journal.models.toolrun_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='ToolRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputRuns', models.ManyToManyField(to='journal.RunEntry')),
            ],
        ),
        migrations.AlterModelOptions(
            name='journalentry',
            options={'ordering': ['-posted'], 'verbose_name_plural': 'journal entries'},
        ),
        migrations.AddField(
            model_name='outputimage',
            name='toolrun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.ToolRun'),
        ),
        migrations.CreateModel(
            name='AnalysisTool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='toolrun',
            name='tool',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='journal.AnalysisTool'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='runentry',
            options={'verbose_name_plural': 'run entries'},
        ),
        migrations.AddField(
            model_name='journalentry',
            name='posted_by',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
