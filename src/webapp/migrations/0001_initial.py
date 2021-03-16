# Generated by Django 3.1.5 on 2021-03-12 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptionOfImprovements',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('design_style', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('effective_age', models.IntegerField(blank=True, null=True)),
                ('walls', models.CharField(blank=True, max_length=50, null=True)),
                ('roof_surface', models.CharField(blank=True, max_length=50, null=True)),
                ('gutters_downspouts', models.CharField(blank=True, max_length=50, null=True)),
                ('win_type', models.CharField(blank=True, max_length=50, null=True)),
                ('storm_screens', models.CharField(blank=True, max_length=50, null=True)),
                ('roof_insulation', models.BooleanField()),
                ('ceiling_insulation', models.BooleanField()),
                ('walls_insulation', models.BooleanField()),
                ('floor_insulation', models.BooleanField()),
                ('none_insulation', models.BooleanField()),
                ('unknown_insulation', models.BooleanField()),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street_address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=50, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
                ('county', models.CharField(blank=True, max_length=100, null=True)),
                ('appraisal_status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Done', 'Done')], default='Not Started', max_length=15)),
                ('comments', models.TextField(blank=True, null=True)),
                ('appraiser', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appraiser', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialsAndCondition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('condition_floors', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('material_floors', models.CharField(blank=True, max_length=50, null=True)),
                ('condition_walls', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('material_walls', models.CharField(blank=True, max_length=50, null=True)),
                ('condition_trim', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('material_trim', models.CharField(blank=True, max_length=50, null=True)),
                ('condition_bath_floor', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('material_bath_floor', models.CharField(blank=True, max_length=50, null=True)),
                ('condition_bath_wainscot', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('material_bath_wainscot', models.CharField(blank=True, max_length=50, null=True)),
                ('condition_doors', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('material_doors', models.CharField(blank=True, max_length=50, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='Utilities',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('heat_type', models.TextField(blank=True, max_length=20, null=True)),
                ('washer_dryer', models.BooleanField()),
                ('heat_fuel', models.CharField(blank=True, max_length=20, null=True)),
                ('heat_condition', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('cooling_type', models.CharField(blank=True, max_length=20, null=True)),
                ('cooling_condition', models.TextField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=10, null=True)),
                ('comments', models.TextField()),
                ('materials_conditions', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.materialsandcondition')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dimensions', models.CharField(blank=True, max_length=30, null=True)),
                ('site_area', models.IntegerField(blank=True, null=True)),
                ('specific_zone', models.CharField(blank=True, max_length=50, null=True)),
                ('zone_compliance', models.CharField(blank=True, choices=[('Legal', 'Legal'), ('Legal Nonconforming (grandfathered use)', 'Legal Nonconf'), ('Illegal', 'Illegal'), ('No Zoning', 'No Zone')], max_length=60, null=True)),
                ('corner_lot', models.BooleanField()),
                ('public_electric', models.BooleanField()),
                ('public_gas', models.BooleanField()),
                ('public_water', models.BooleanField()),
                ('public_sanitary_sewer', models.BooleanField()),
                ('public_storm_sewer', models.BooleanField()),
                ('fema_flood_hazard', models.BooleanField()),
                ('topography', models.CharField(blank=True, max_length=30, null=True)),
                ('size', models.CharField(blank=True, max_length=30, null=True)),
                ('shape', models.CharField(blank=True, max_length=30, null=True)),
                ('drainage', models.CharField(blank=True, max_length=30, null=True)),
                ('view', models.CharField(blank=True, max_length=30, null=True)),
                ('landscaping', models.CharField(blank=True, max_length=30, null=True)),
                ('driveway_surface', models.CharField(blank=True, max_length=30, null=True)),
                ('apparent_easements', models.CharField(blank=True, max_length=30, null=True)),
                ('fema_zone', models.CharField(blank=True, max_length=30, null=True)),
                ('fema_map_no', models.CharField(blank=True, max_length=30, null=True)),
                ('map_date', models.DateField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='RoomSummary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num_bedrooms', models.IntegerField(blank=True, null=True)),
                ('num_bathrooms', models.FloatField(blank=True, null=True)),
                ('num_floors', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_type', models.CharField(blank=True, choices=[('Foyer', 'Foyer'), ('Living Room', 'Living'), ('Dining Room', 'Dining'), ('Kitchen', 'Kitchen'), ('Den', 'Den'), ('Family Room', 'Family'), ('Recreation Room', 'Recreation'), ('Bedroom', 'Bedroom'), ('Bathroom', 'Bath'), ('Half bath', 'Halfbath'), ('Laundry Room', 'Laundry'), ('Basement', 'Basement'), ('Other', 'Other')], max_length=20, null=True)),
                ('room_level', models.IntegerField(blank=True, null=True)),
                ('room_area', models.IntegerField(blank=True, null=True)),
                ('room_comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('borrower', models.CharField(blank=True, max_length=50, null=True)),
                ('current_owner', models.CharField(blank=True, max_length=50, null=True)),
                ('occupant', models.CharField(blank=True, choices=[('Owner', 'Owner'), ('Tenant', 'Tenant'), ('Vacant', 'Vacant')], max_length=10, null=True)),
                ('tax_year', models.IntegerField(blank=True, choices=[(2022, 2022), (2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985)], null=True)),
                ('re_taxes', models.IntegerField(blank=True, null=True)),
                ('prop_rights_appraised', models.CharField(blank=True, choices=[('Fee Simple', 'Fee Simple'), ('Leasehold', 'Leasehold')], max_length=10, null=True)),
                ('project_type', models.CharField(blank=True, choices=[('Planned Unit Development', 'Pud'), ('Condominium', 'Condominium')], max_length=30, null=True)),
                ('hoa_price', models.IntegerField(blank=True, null=True)),
                ('map_ref', models.IntegerField(blank=True, null=True)),
                ('census_tract', models.IntegerField(blank=True, null=True)),
                ('sale_price', models.IntegerField(blank=True, null=True)),
                ('date_of_sale', models.DateField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('role', models.TextField(choices=[('APPRAISER', 'Appraiser'), ('CUSTOMER', 'Customer requesting appraisal')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offsite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('offsite_curb_note', models.CharField(blank=True, max_length=50, null=True)),
                ('offsite_street_note', models.CharField(blank=True, max_length=50, null=True)),
                ('offsite_sidewalk_note', models.CharField(blank=True, max_length=50, null=True)),
                ('offsite_streetlight_note', models.CharField(blank=True, max_length=50, null=True)),
                ('offsite_alley_note', models.CharField(blank=True, max_length=50, null=True)),
                ('offsite_streetlights', models.CharField(blank=True, choices=[('Public', 'Public'), ('Private', 'Private'), ('Neither', 'Neither')], max_length=10, null=True)),
                ('offsite_curb', models.CharField(blank=True, choices=[('Public', 'Public'), ('Private', 'Private'), ('Neither', 'Neither')], max_length=10, null=True)),
                ('offsite_sidewalk', models.CharField(blank=True, choices=[('Public', 'Public'), ('Private', 'Private'), ('Neither', 'Neither')], max_length=10, null=True)),
                ('offsite_alley', models.CharField(blank=True, choices=[('Public', 'Public'), ('Private', 'Private'), ('Neither', 'Neither')], max_length=10, null=True)),
                ('offsite_street', models.CharField(blank=True, choices=[('Public', 'Public'), ('Private', 'Private'), ('Neither', 'Neither')], max_length=10, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(blank=True, choices=[('Urban', 'Urban'), ('Suburban', 'Suburban'), ('Rural', 'Rural')], max_length=10, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('built_up', models.CharField(blank=True, choices=[('Over 75%', 'Over 75%'), ('ABOVE25', '25%-75%'), ('UNDER25', 'Under 25%')], max_length=15, null=True)),
                ('growth_rate', models.CharField(blank=True, choices=[('Rapid', 'Rapid'), ('Stable', 'Stable'), ('Slow', 'Slow')], max_length=10, null=True)),
                ('property_value', models.CharField(blank=True, choices=[('Increasing', 'Increasing'), ('Stable', 'Stable'), ('Slow', 'Slow')], max_length=15, null=True)),
                ('demand_supply', models.CharField(blank=True, choices=[('Shortage', 'Shortage'), ('Stable', 'Stable'), ('Declining', 'Declining')], max_length=20, null=True)),
                ('marketability_factors', models.TextField(blank=True, null=True)),
                ('market_conditions', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='Foundation',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('sump_pump', models.BooleanField()),
                ('foundation_ext', models.TextField(blank=True, null=True)),
                ('slab', models.BooleanField()),
                ('crawl_space', models.BooleanField()),
                ('dampness', models.TextField(blank=True, null=True)),
                ('infestation', models.TextField(blank=True, null=True)),
                ('settlement', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('improvements_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.descriptionofimprovements')),
            ],
        ),
        migrations.AddField(
            model_name='descriptionofimprovements',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house'),
        ),
        migrations.CreateModel(
            name='Basement',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('basement_area', models.IntegerField(blank=True, null=True)),
                ('basement_percent_finished', models.TextField(blank=True, null=True)),
                ('basement_ceiling', models.TextField(blank=True, null=True)),
                ('basement_walls', models.TextField(blank=True, null=True)),
                ('basement_floor', models.TextField(blank=True, null=True)),
                ('basement_outside_entry', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('materials_conditions', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.materialsandcondition')),
            ],
        ),
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('positive_features', models.TextField(blank=True, null=True)),
                ('negative_conditions', models.TextField(blank=True, null=True)),
                ('reconciliation', models.TextField(blank=True, null=True)),
                ('appraisal_price', models.IntegerField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pool', models.CharField(blank=True, max_length=50, null=True)),
                ('fireplace', models.CharField(blank=True, max_length=50, null=True)),
                ('patio', models.CharField(blank=True, max_length=50, null=True)),
                ('deck', models.CharField(blank=True, max_length=50, null=True)),
                ('porch', models.CharField(blank=True, max_length=50, null=True)),
                ('fence', models.CharField(blank=True, max_length=50, null=True)),
                ('garage', models.CharField(blank=True, max_length=50, null=True)),
                ('basement', models.CharField(blank=True, max_length=50, null=True)),
                ('attic', models.CharField(blank=True, max_length=50, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.house')),
            ],
        ),
    ]
