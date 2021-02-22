# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Basement(models.Model):
    id = models.IntegerField(primary_key=True)
    basement_area = models.IntegerField(blank=True, null=True)
    basement_percent_finished = models.TextField(blank=True, null=True)
    basement_ceiling = models.TextField(blank=True, null=True)
    basement_walls = models.TextField(blank=True, null=True)
    basement_floor = models.TextField(blank=True, null=True)
    basement_outside_entry = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    materials_conditions = models.ForeignKey('MaterialsAndCondition', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'basement'


class DescriptionOfImprovements(models.Model):
    id = models.IntegerField(primary_key=True)
    design_style = models.TextField(blank=True, null=True)
    age = models.IntegerField()
    effective_age = models.IntegerField(blank=True, null=True)
    walls = models.TextField(blank=True, null=True)
    roof_surface = models.TextField(blank=True, null=True)
    gutters_downspouts = models.TextField(blank=True, null=True)
    win_type = models.TextField(blank=True, null=True)
    storm_screens = models.TextField(blank=True, null=True)
    roof_insulation = models.BooleanField()
    ceiling_insulation = models.BooleanField()
    walls_insulation = models.BooleanField()
    floor_insulation = models.BooleanField()
    none_insulation = models.BooleanField()
    unknown_insulation = models.BooleanField()
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey('House', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'description_of_improvements'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Foundation(models.Model):
    id = models.IntegerField(primary_key=True)
    sump_pump = models.BooleanField()
    foundation_ext = models.TextField(blank=True, null=True)
    slab = models.BooleanField()
    crawl_space = models.BooleanField()
    dampness = models.TextField(blank=True, null=True)
    infestation = models.TextField(blank=True, null=True)
    settlement = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    improvements = models.ForeignKey(DescriptionOfImprovements, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'foundation'


class House(models.Model):
    id = models.IntegerField(primary_key=True)
    street_address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()
    county = models.TextField()
    appraisal_status = models.TextField()  # This field type is a guess.
    appraiser = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'house'


class HouseFeatures(models.Model):
    id = models.IntegerField(primary_key=True)
    pool = models.TextField()
    fireplace = models.TextField()
    patio = models.TextField()
    deck = models.TextField()
    fence = models.TextField()
    garage = models.TextField()
    basement = models.TextField()
    attic = models.TextField()
    comments = models.TextField()
    house = models.ForeignKey(House, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'house_features'


class Kitchen(models.Model):
    id = models.IntegerField(primary_key=True)
    kitchen_refrig = models.BooleanField()
    kitchen_oven = models.BooleanField()
    kitchen_disposal = models.BooleanField()
    kitchen_dishwasher = models.BooleanField()
    kitchen_fan_hood = models.BooleanField()
    kitchen_microwave = models.BooleanField()
    kitchen_description = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    materials_condition = models.ForeignKey('MaterialsAndCondition', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kitchen'


class MaterialsAndCondition(models.Model):
    id = models.IntegerField(primary_key=True)
    condition_floors = models.TextField(blank=True, null=True)  # This field type is a guess.
    material_floors = models.TextField(blank=True, null=True)
    condition_walls = models.TextField(blank=True, null=True)  # This field type is a guess.
    material_walls = models.TextField(blank=True, null=True)
    condition_trim = models.TextField(blank=True, null=True)  # This field type is a guess.
    materials_trim = models.TextField(blank=True, null=True)
    condition_bath_floor = models.TextField(blank=True, null=True)  # This field type is a guess.
    materials_bath_floor = models.TextField(blank=True, null=True)
    condition_bath_wainscot = models.TextField(blank=True, null=True)  # This field type is a guess.
    materials_bath_wainscot = models.TextField(blank=True, null=True)
    condition_doors = models.TextField(blank=True, null=True)  # This field type is a guess.
    materials_doors = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'materials_and_condition'


class Neighborhood(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.TextField()  # This field type is a guess.
    name = models.IntegerField()
    built_up = models.TextField()  # This field type is a guess.
    growth_rate = models.TextField()  # This field type is a guess.
    property_value = models.TextField()  # This field type is a guess.
    demand_supply = models.TextField()  # This field type is a guess.
    marketability_factors = models.TextField()
    market_conditions = models.TextField()
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'neighborhood'


class Offsite(models.Model):
    id = models.IntegerField(primary_key=True)
    offsite_curb_note = models.TextField(blank=True, null=True)
    offsite_street_note = models.TextField(blank=True, null=True)
    offsite_sidewalk_note = models.TextField(blank=True, null=True)
    offsite_streetlight_note = models.TextField(blank=True, null=True)
    offsite_alley_note = models.TextField(blank=True, null=True)
    offsite_streetlights = models.TextField()  # This field type is a guess.
    offsite_curb = models.TextField()  # This field type is a guess.
    offsite_sidewalk = models.TextField()  # This field type is a guess.
    offsite_alley = models.TextField()  # This field type is a guess.
    offsite_street = models.TextField()  # This field type is a guess.
    comments = models.TextField(blank=True, null=True)
    site = models.ForeignKey('Site', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'offsite'


class Property(models.Model):
    id = models.IntegerField(primary_key=True)
    borrower = models.TextField()
    current_owner = models.TextField()
    occupant = models.TextField(blank=True, null=True)  # This field type is a guess.
    tax_year = models.IntegerField(blank=True, null=True)
    re_taxes = models.IntegerField(blank=True, null=True)
    prop_rights_appraised = models.TextField(blank=True, null=True)  # This field type is a guess.
    project_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    hoa_price = models.IntegerField(blank=True, null=True)
    map_ref = models.IntegerField(blank=True, null=True)
    census_tract = models.IntegerField(blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)
    date_of_sale = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'property'


class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    room_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    room_level = models.IntegerField(blank=True, null=True)
    room_area = models.IntegerField(blank=True, null=True)
    room_comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'room'


class Site(models.Model):
    id = models.IntegerField(primary_key=True)
    dimensions = models.TextField(blank=True, null=True)
    site_area = models.IntegerField(blank=True, null=True)
    specific_zone = models.TextField(blank=True, null=True)
    zone_compliance = models.TextField(blank=True, null=True)  # This field type is a guess.
    corner_lot = models.BooleanField()
    public_electric = models.BooleanField()
    public_gas = models.BooleanField()
    public_water = models.BooleanField()
    public_sanitary_sewer = models.BooleanField()
    public_storm_sewer = models.BooleanField()
    topography = models.TextField(blank=True, null=True)
    size = models.TextField(blank=True, null=True)
    shape = models.TextField(blank=True, null=True)
    drainage = models.TextField(blank=True, null=True)
    view = models.TextField(blank=True, null=True)
    landscaping = models.TextField(blank=True, null=True)
    driveway_surface = models.TextField(blank=True, null=True)
    apparent_easements = models.TextField(blank=True, null=True)
    fema_flood_hazard = models.BooleanField(blank=True, null=True)
    fema_zone = models.TextField(blank=True, null=True)
    fema_map_no = models.TextField(blank=True, null=True)
    map_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'site'


class Utilities(models.Model):
    id = models.IntegerField(primary_key=True)
    heat_type = models.TextField()
    washer_dryer = models.BooleanField()
    heat_fuel = models.TextField()
    heat_condition = models.TextField()  # This field type is a guess.
    cooling_type = models.TextField()
    cooling_condition = models.TextField()  # This field type is a guess.
    comments = models.TextField()
    materials_conditions = models.ForeignKey(MaterialsAndCondition, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'utilities'


class WebappAppraisal(models.Model):
    id = models.IntegerField(primary_key=True)
    house = models.ForeignKey(House, models.DO_NOTHING)
    positive_features = models.TextField(blank=True, null=True)
    negative_conditions = models.TextField(blank=True, null=True)
    reconciliation = models.TextField(blank=True, null=True)
    appraisal_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'webapp_appraisal'


class WebappProfile(models.Model):
    phone_number = models.CharField(max_length=20)
    role = models.TextField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'webapp_profile'
