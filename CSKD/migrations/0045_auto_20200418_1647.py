# Generated by Django 3.0.4 on 2020-04-18 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSKD', '0044_auto_20200418_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestnews',
            name='Slug',
            field=models.SlugField(default='2020-04-18_16_47_32', unique=True, verbose_name='Slug'),
        ),
    ]
