# Generated by Django 3.1.5 on 2021-03-10 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0025_auto_20210310_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offsite',
            name='house',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house'),
        ),
    ]
