# Generated by Django 3.1.5 on 2021-02-19 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20210211_2344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('house_id', models.IntegerField()),
                ('positive_features', models.TextField(blank=True, null=True)),
                ('negative_conditions', models.TextField(blank=True, null=True)),
                ('reconciliation', models.TextField(blank=True, null=True)),
                ('appraisal_price', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]