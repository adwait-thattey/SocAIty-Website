# Generated by Django 2.1.2 on 2018-10-18 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='github_url',
            field=models.URLField(blank=True, verbose_name='Github Profile Url'),
        ),
    ]