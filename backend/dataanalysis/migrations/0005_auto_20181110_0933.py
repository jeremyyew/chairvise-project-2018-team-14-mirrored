# Generated by Django 2.1.3 on 2018-11-10 09:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dataanalysis', '0004_auto_20181110_0918'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercsvfile',
            unique_together={('user', 'csv_file')},
        ),
    ]
