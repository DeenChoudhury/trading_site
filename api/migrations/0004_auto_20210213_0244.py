# Generated by Django 3.1.6 on 2021-02-13 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210213_0218'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalystRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('ticker', models.CharField(max_length=5)),
                ('company', models.CharField(max_length=30)),
                ('action', models.CharField(max_length=30)),
                ('brokerage', models.CharField(max_length=30)),
                ('current', models.FloatField()),
                ('target_original', models.FloatField()),
                ('target_new', models.FloatField()),
                ('rating', models.CharField(max_length=30)),
                ('impact', models.CharField(max_length=30)),
                ('percent_upside', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]