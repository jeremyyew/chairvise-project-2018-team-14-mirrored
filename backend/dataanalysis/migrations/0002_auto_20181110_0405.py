# Generated by Django 2.1.3 on 2018-11-10 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataanalysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='person_id',
            field=models.IntegerField(null=True, verbose_name='author unique id'),
        ),
    ]
