# Generated by Django 3.1.5 on 2021-03-05 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_auto_20210305_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenities',
            name='porch',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
