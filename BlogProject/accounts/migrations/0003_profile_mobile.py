# Generated by Django 3.0 on 2020-01-11 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200104_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobile',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
