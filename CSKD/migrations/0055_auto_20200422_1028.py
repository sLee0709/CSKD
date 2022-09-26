# Generated by Django 3.0.4 on 2020-04-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSKD', '0054_auto_20200418_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugs',
            name='Drug_target',
            field=models.CharField(default='N/A', max_length=150, verbose_name='Targets'),
        ),
        migrations.AlterField(
            model_name='latestnews',
            name='Slug',
            field=models.SlugField(default='2020-04-22_10_28_52', unique=True, verbose_name='Slug'),
        ),
    ]
