# Generated by Django 3.0.4 on 2020-09-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSKD', '0073_auto_20200730_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cases',
            name='Disease',
        ),
        migrations.AddField(
            model_name='cases',
            name='Disease',
            field=models.CharField(blank=True, max_length=150, verbose_name='Diseases'),
        ),
        migrations.AlterField(
            model_name='latestnews',
            name='Slug',
            field=models.SlugField(default='2020-09-07_15_30_04', unique=True, verbose_name='Slug'),
        ),
    ]
