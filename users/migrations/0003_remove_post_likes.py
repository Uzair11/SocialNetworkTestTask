# Generated by Django 3.1.5 on 2022-02-05 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
