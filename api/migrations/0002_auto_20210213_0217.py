# Generated by Django 3.1.6 on 2021-02-13 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='name',
            new_name='test',
        ),
    ]
