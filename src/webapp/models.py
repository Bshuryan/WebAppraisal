from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False


class Profile(models.Model):
    class Roles(models.TextChoices):
        APPRAISER = 'APPRAISER', _('Appraiser')
        CUSTOMER = 'CUSTOMER', _('Customer requesting appraisal')

    def get_display_role(self):
        if self.role == Profile.Roles.APPRAISER:
            return 'Appraiser'
        else:
            return 'Customer requesting appraisal'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.TextField(choices=Roles.choices, blank=False)


class House(models.Model):
    id = models.IntegerField(primary_key=True)
    street_address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()
    county = models.TextField()
    appraisal_status = models.TextField()
    appraiser = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)


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


class MaterialsAndCondition(models.Model):
    class Condition(models.TextChoices):
        GOOD = 'GOOD', _('Good')
        AVERAGE = 'AVERAGE', _('Average')
        POOR = 'POOR', _('Poor')

    id = models.IntegerField(primary_key=True)
    condition_floors = models.TextField(choices=Condition.choices, blank=False)
    material_floors = models.TextField(blank=True, null=True)
    condition_walls = models.TextField(choices=Condition.choices, blank=False)
    material_walls = models.TextField(blank=True, null=True)
    condition_trim = models.TextField(choices=Condition.choices, blank=False)
    materials_trim = models.TextField(blank=True, null=True)
    condition_bath_floor = models.TextField(choices=Condition.choices, blank=False)
    materials_bath_floor = models.TextField(blank=True, null=True)
    condition_bath_wainscot = models.TextField(choices=Condition.choices, blank=False)
    materials_bath_wainscot = models.TextField(blank=True, null=True)
    condition_doors = models.TextField(choices=Condition.choices, blank=False)
    materials_doors = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)


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


class Property(models.Model):
    id = models.IntegerField(primary_key=True)
    borrower = models.TextField()
    current_owner = models.TextField()
    occupant = models.TextField(blank=True, null=True)
    tax_year = models.IntegerField(blank=True, null=True)
    re_taxes = models.IntegerField(blank=True, null=True)
    prop_rights_appraised = models.TextField(blank=True, null=True)
    project_type = models.TextField(blank=True, null=True)
    hoa_price = models.IntegerField(blank=True, null=True)
    map_ref = models.IntegerField(blank=True, null=True)
    census_tract = models.IntegerField(blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)
    date_of_sale = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)


class Room(models.Model):
    class RoomType(models.TextChoices):
        FOYER = 'FOYER', _('Foyer')
        LIVING = 'LIVING', _('Living Room')
        DINING = 'DINING', _('Dining Room')
        KITCHEN = 'KITCHEN', _('Kitchen')
        DEN = 'DEN', _('Den')
        FAMILY = 'FAMILY', _('Family Room')
        RECREATION = 'RECREATION', _('Recreation Room')
        BEDROOM = 'BEDROOM', _('Bedroom')
        BATH = 'BATH', _('Bath')
        HALF_BATH = 'HALF_BATH', _('Half Bath')
        LAUNDRY = 'LAUNDRY', _('Laundry')
        BASEMENT = 'BASEMENT', _('Basement')

    id = models.IntegerField(primary_key=True)
    room_type = models.TextField(choices=RoomType.choices, blank=False)
    room_level = models.IntegerField(blank=True, null=True)
    room_area = models.IntegerField(blank=True, null=True)
    room_comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)


class Site(models.Model):
    class ZoneCompliance(models.TextChoices):
        LEGAL = 'LEGAL', _('LEGAL')
        LEGAL_NONCONF = 'LEGAL_NONCONF', _('Legal Nonconforming (grandfathered use)')
        ILLEGAL = 'ILLEGAL', _('Illegal')
        NO_ZONING = 'NO_ZONING', _('No Zoning')

    id = models.IntegerField(primary_key=True)
    dimensions = models.TextField(blank=True, null=True)
    site_area = models.IntegerField(blank=True, null=True)
    specific_zone = models.TextField(blank=True, null=True)
    zone_compliance = models.TextField(choices=ZoneCompliance.choices, blank=False)
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


class Offsite(models.Model):
    class OffsiteType(models.TextChoices):
        PUBLIC = 'PUBLIC', _('Public')
        PRIVATE = 'PRIVATE', _('Private')
        NEITHER = 'NEITHER', _('Neither')

    id = models.IntegerField(primary_key=True)
    offsite_curb_note = models.TextField(blank=True, null=True)
    offsite_street_note = models.TextField(blank=True, null=True)
    offsite_sidewalk_note = models.TextField(blank=True, null=True)
    offsite_streetlight_note = models.TextField(blank=True, null=True)
    offsite_alley_note = models.TextField(blank=True, null=True)
    offsite_streetlights = models.TextField(choices=OffsiteType.choices, blank=False)
    offsite_curb = models.TextField(choices=OffsiteType.choices, blank=False)
    offsite_sidewalk = models.TextField(choices=OffsiteType.choices, blank=False)
    offsite_alley = models.TextField(choices=OffsiteType.choices, blank=False)
    offsite_street = models.TextField(choices=OffsiteType.choices, blank=False)
    comments = models.TextField(blank=True, null=True)
    site = models.ForeignKey('Site', models.DO_NOTHING)


class Utilities(models.Model):
    class Condition(models.TextChoices):
        GOOD = 'GOOD', _('Good')
        AVERAGE = 'AVERAGE', _('Average')
        POOR = 'POOR', _('Poor')

    id = models.IntegerField(primary_key=True)
    heat_type = models.TextField()
    washer_dryer = models.BooleanField()
    heat_fuel = models.TextField()
    heat_condition = models.TextField(choices=Condition.choices, blank=False)
    cooling_type = models.TextField()
    cooling_condition = models.TextField(choices=Condition.choices, blank=False)
    comments = models.TextField()
    materials_conditions = models.ForeignKey(MaterialsAndCondition, models.DO_NOTHING)


class Appraisal(models.Model):
    id = models.IntegerField(primary_key=True)
    house = models.ForeignKey(House, models.DO_NOTHING)
    positive_features = models.TextField(blank=True, null=True)
    negative_conditions = models.TextField(blank=True, null=True)
    reconciliation = models.TextField(blank=True, null=True)
    appraisal_price = models.IntegerField(blank=True, null=True)


class Neighborhood(models.Model):
    class Location(models.TextChoices):
        URBAN = 'URBAN', _('Urban')
        SUBURBAN = 'SUBURBAN', _('Suburban')
        RURAL = 'RURAL', _('Rural')

    class GrowthRate(models.TextChoices):
        RAPID = 'RAPID', _('Rapid')
        STABLE = 'STABLE', _('Stable')
        SLOW = 'SLOW', _('Slow')

    class BuiltUp(models.TextChoices):
        OVER75 = 'OVER75', _('Over 75%')
        UNDER75 = 'UNDER75', _('25%-75%')
        UNDER25 = 'UNDER25', _('Under 25%')

    class SupplyDemand(models.TextChoices):
        SHORTAGE = 'SHORTAGE', _('Shortage')
        STABLE = 'STABLE', _('Stable')
        DECLINING = 'DECLINING', _('Declining')

    id = models.IntegerField(primary_key=True)
    location = models.TextField(choices=Location.choices, blank=False)
    name = models.IntegerField()
    built_up = models.TextField(choices=BuiltUp.choices, blank=False)
    growth_rate = models.TextField(choices=GrowthRate.choices, blank=False)
    property_value = models.TextField()
    supply_demand = models.TextField(choices=SupplyDemand.choices, blank=False)
    marketability_factors = models.TextField()
    market_conditions = models.TextField()
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)
