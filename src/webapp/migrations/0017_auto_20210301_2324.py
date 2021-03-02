# Generated by Django 3.1.5 on 2021-03-01 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_auto_20210301_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descriptionofimprovements',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='condition_bath_floor',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='condition_bath_wainscot',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='condition_doors',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='condition_floors',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='condition_trim',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='condition_walls',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='material_floors',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='material_walls',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='materials_bath_floor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='materials_bath_wainscot',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='materials_doors',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='materialsandcondition',
            name='materials_trim',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(blank=True, choices=[('Foyer', 'Foyer'), ('Living Room', 'Living'), ('Dining Room', 'Dining'), ('Kitchen', 'Kitchen'), ('Den', 'Den'), ('Family Room', 'Family'), ('Recreation Room', 'Recreation'), ('Bedroom', 'Bedroom'), ('Bathroom', 'Bath'), ('1/2 bath', 'Halfbath'), ('Laundry Room', 'Laundry'), ('Basement', 'Basement')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='fema_flood_hazard',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='utilities',
            name='cooling_condition',
            field=models.TextField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='utilities',
            name='cooling_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='utilities',
            name='heat_condition',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='utilities',
            name='heat_fuel',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='utilities',
            name='heat_type',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
    ]
