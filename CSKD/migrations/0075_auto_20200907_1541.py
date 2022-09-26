# Generated by Django 3.0.4 on 2020-09-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSKD', '0074_auto_20200907_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cases',
            name='Drug_for_treatment',
        ),
        migrations.AddField(
            model_name='cases',
            name='Drug_for_treatment',
            field=models.CharField(blank=True, max_length=100, verbose_name='Drugs'),
        ),
        migrations.AlterField(
            model_name='latestnews',
            name='Slug',
            field=models.SlugField(default='2020-09-07_15_41_07', unique=True, verbose_name='Slug'),
        ),
    ]
