# Generated by Django 2.1.2 on 2018-10-18 19:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20181018_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date Published'),
        ),
    ]
