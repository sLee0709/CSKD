# Generated by Django 3.0.4 on 2020-04-17 15:21

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('CSKD', '0025_auto_20200417_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drugs',
            name='Structure',
            field=imagekit.models.fields.ProcessedImageField(default='dryg_imgs/404.jpg', upload_to='drug_imgs', verbose_name='Structure'),
        ),
        migrations.AlterField(
            model_name='latestnews',
            name='Slug',
            field=models.SlugField(default='2020-04-17_15_21_14', unique=True, verbose_name='Slug'),
        ),
    ]
