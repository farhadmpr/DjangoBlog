# Generated by Django 3.0 on 2019-12-24 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20191222_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='view_count',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
