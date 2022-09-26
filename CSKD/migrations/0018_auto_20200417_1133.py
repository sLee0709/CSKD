# Generated by Django 3.0.4 on 2020-04-17 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSKD', '0017_auto_20200417_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cytoinfo',
            name='PMID',
        ),
        migrations.AddField(
            model_name='cytoinfo',
            name='PMID',
            field=models.CharField(default='N/A', max_length=100, verbose_name='PMID'),
        ),
        migrations.AlterField(
            model_name='latestnews',
            name='Slug',
            field=models.SlugField(default='2020-04-17_11_33_58', unique=True, verbose_name='Slug'),
        ),
        migrations.DeleteModel(
            name='Cases',
        ),
    ]
