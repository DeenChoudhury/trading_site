# Generated by Django 3.1.6 on 2021-02-13 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210213_0217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='test',
            new_name='data',
        ),
    ]
