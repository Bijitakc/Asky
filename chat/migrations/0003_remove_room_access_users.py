# Generated by Django 3.2.6 on 2021-09-07 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='access_users',
        ),
    ]