# Generated by Django 3.1.5 on 2021-04-25 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20210422_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='re_taxes',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
