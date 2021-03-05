import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from localflavor.us.us_states import STATE_CHOICES

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
    class AppraisalStatus(models.TextChoices):
        NOT_STARTED = 'Not Started'
        IN_PROGRESS = 'In Progress'
        DONE = 'Done'

    id = models.AutoField(primary_key=True)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(blank=True, null=True, max_length=50, choices=STATE_CHOICES)
    zip = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    appraisal_status = models.CharField(default=AppraisalStatus.NOT_STARTED, choices=AppraisalStatus.choices, max_length=15)
    appraiser = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False, related_name='appraiser')
    customer = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False, related_name='customer')
    comments = models.TextField(blank=True, null=True)

class DescriptionOfImprovements(models.Model):
    id = models.AutoField(primary_key=True)
    design_style = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    effective_age = models.IntegerField(blank=True, null=True)
    walls = models.CharField(max_length=50, blank=True, null=True)
    roof_surface = models.CharField(max_length=50, blank=True, null=True)
    gutters_downspouts = models.CharField(max_length=50, blank=True, null=True)
    win_type = models.CharField(max_length=50, blank=True, null=True)
    storm_screens = models.CharField(max_length=50, blank=True, null=True)
    roof_insulation = models.BooleanField()
    ceiling_insulation = models.BooleanField()
    walls_insulation = models.BooleanField()
    floor_insulation = models.BooleanField()
    none_insulation = models.BooleanField()
    unknown_insulation = models.BooleanField()
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

class MaterialsAndCondition(models.Model):
    class Condition(models.TextChoices):
        GOOD = 'Good'
        AVERAGE = 'Average'
        POOR = 'Poor'
    id = models.AutoField(primary_key=True)
    condition_floors = models.CharField(max_length=10,blank=True, null=True, choices=Condition.choices)
    material_floors = models.CharField(max_length=50, blank=True, null=True)
    condition_walls = models.CharField(max_length=10,blank=True, null=True, choices=Condition.choices)
    material_walls = models.CharField(max_length=50, blank=True, null=True)
    condition_trim = models.CharField(max_length=10,blank=True, null=True, choices=Condition.choices)
    material_trim = models.CharField(max_length=50, blank=True, null=True)
    condition_bath_floor = models.CharField(max_length=10,blank=True, null=True, choices=Condition.choices)
    material_bath_floor = models.CharField(max_length=50, blank=True, null=True)
    condition_bath_wainscot = models.CharField(max_length=10,blank=True, null=True, choices=Condition.choices)
    material_bath_wainscot = models.CharField(max_length=50, blank=True, null=True)
    condition_doors = models.CharField(max_length=10,blank=True, null=True, choices=Condition.choices)
    material_doors = models.CharField(max_length=50, blank=True, null=True)
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

class Property(models.Model):
    class OccupantTypes(models.TextChoices):
        OWNER = 'Owner'
        TENANT = 'Tenant'
        VACANT = 'Vacant'

    class PropRightsAppraisedTypes(models.TextChoices):
        FEE_SIMPLE = 'Fee Simple'
        LEASEHOLD = 'Leasehold'

    class ProjectTypes(models.TextChoices):
        PUD = 'Planned Unit Development'
        CONDOMINIUM = 'Condominium'

    year_choices = [(i, i) for i in range(datetime.date.today().year+1, 1984, -1)]

    id = models.AutoField(primary_key=True)
    borrower = models.CharField(max_length=50, blank=True, null=True)
    current_owner = models.CharField(max_length=50, blank=True, null=True)
    occupant = models.CharField(max_length=10, blank=True, null=True, choices=OccupantTypes.choices)  # This field type is a guess.
    tax_year = models.IntegerField(blank=True, null=True, choices=year_choices)
    re_taxes = models.IntegerField(blank=True, null=True)
    prop_rights_appraised = models.CharField(max_length=10, blank=True, null=True, choices=PropRightsAppraisedTypes.choices)  # This field type is a guess.
    project_type = models.CharField(max_length=30, blank=True, null=True, choices=ProjectTypes.choices)  # This field type is a guess.
    hoa_price = models.IntegerField(blank=True, null=True)
    map_ref = models.IntegerField(blank=True, null=True)
    census_tract = models.IntegerField(blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)
    date_of_sale = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

class RoomSummary(models.Model):
    id = models.AutoField(primary_key=True)
    num_bedrooms = models.IntegerField(blank=True, null=True)
    num_bathrooms = models.FloatField(blank=True, null=True)
    num_floors = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

class Room(models.Model):
    class RoomType(models.TextChoices):
        FOYER = 'Foyer'
        LIVING = 'Living Room'
        DINING = 'Dining Room'
        KITCHEN = 'Kitchen'
        DEN = 'Den'
        FAMILY = 'Family Room'
        RECREATION = 'Recreation Room'
        BEDROOM = 'Bedroom'
        BATH = 'Bathroom'
        HALFBATH = 'Half bath'
        LAUNDRY = 'Laundry Room'
        BASEMENT = 'Basement'
        OTHER = 'Other'

    id = models.AutoField(primary_key=True)
    room_type = models.CharField(max_length=20, blank=True, null=True, choices=RoomType.choices)
    room_level = models.IntegerField(blank=True, null=True)
    room_area = models.IntegerField(blank=True, null=True)
    room_comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)
    
class Site(models.Model):
    class ZoneCompliance(models.TextChoices):
        LEGAL = 'Legal'
        LEGAL_NONCONF = 'Legal Nonconforming (grandfathered use)'
        ILLEGAL = 'Illegal'
        NO_ZONE = 'No Zoning'
    id = models.AutoField(primary_key=True)
    dimensions = models.CharField(max_length=30, blank=True, null=True)
    site_area = models.IntegerField(blank=True, null=True)
    specific_zone = models.CharField(max_length=50, blank=True, null=True)
    zone_compliance = models.CharField(max_length=60, blank=True, null=True, choices=ZoneCompliance.choices)
    corner_lot = models.BooleanField()
    public_electric = models.BooleanField()
    public_gas = models.BooleanField()
    public_water = models.BooleanField()
    public_sanitary_sewer = models.BooleanField()
    public_storm_sewer = models.BooleanField()
    fema_flood_hazard = models.BooleanField()
    topography = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    shape = models.CharField(max_length=30, blank=True, null=True)
    drainage = models.CharField(max_length=30, blank=True, null=True)
    view = models.CharField(max_length=30, blank=True, null=True)
    landscaping = models.CharField(max_length=30, blank=True, null=True)
    driveway_surface = models.CharField(max_length=30, blank=True, null=True)
    apparent_easements = models.CharField(max_length=30, blank=True, null=True)

    fema_zone = models.CharField(max_length=30, blank=True, null=True)
    fema_map_no = models.CharField(max_length=30, blank=True, null=True)
    map_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)
    
class Offsite(models.Model):
    class PublicUtilities(models.TextChoices):
        PUBLIC = 'Public'
        PRIVATE = 'Private'
        NEITHER = 'Neither'
    id = models.IntegerField(primary_key=True)
    offsite_curb_note = models.CharField(max_length=50,blank=True, null=True)
    offsite_street_note = models.CharField(max_length=50,blank=True, null=True)
    offsite_sidewalk_note = models.CharField(max_length=50,blank=True, null=True)
    offsite_streetlight_note = models.CharField(max_length=50,blank=True, null=True)
    offsite_alley_note = models.CharField(max_length=50, blank=True, null=True)
    offsite_streetlights = models.CharField(max_length=10, blank= True, null=True, choices=PublicUtilities.choices)
    offsite_curb = models.CharField(max_length=10, blank= True, null=True, choices=PublicUtilities.choices)
    offsite_sidewalk = models.CharField(max_length=10, blank= True, null=True, choices=PublicUtilities.choices)
    offsite_alley = models.CharField(max_length=10, blank= True, null=True, choices=PublicUtilities.choices)
    offsite_street = models.CharField(max_length=10, blank= True, null=True, choices=PublicUtilities.choices)
    comments = models.TextField(blank=True, null=True)
    site = models.ForeignKey('Site', models.DO_NOTHING)

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
    improvements_id = models.ForeignKey(DescriptionOfImprovements, models.DO_NOTHING)
    
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

class Utilities(models.Model):
    class Condition(models.TextChoices):
        GOOD = 'Good'
        AVERAGE = 'Average'
        POOR = 'Poor'
    id = models.IntegerField(primary_key=True)
    heat_type = models.TextField(max_length=20,blank=True, null=True)
    washer_dryer = models.BooleanField()
    heat_fuel = models.CharField(max_length=20,blank=True, null=True)
    heat_condition = models.CharField(max_length=10,blank=True, null=True, choices=Condition.choices)
    cooling_type = models.CharField(max_length=20,blank=True, null=True)
    cooling_condition = models.TextField(max_length=10,blank=True, null=True, choices=Condition.choices)
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
        URBAN = 'Urban'
        SUBURBAN = 'Suburban'
        RURAL = 'Rural'

    class GrowthRate(models.TextChoices):
        RAPID = 'Rapid'
        STABLE = 'Stable'
        SLOW = 'Slow'

    class BuiltUp(models.TextChoices):
        OVER75 = 'Over 75%', _('Over 75%')
        ABOVE25= 'ABOVE25' , _('25%-75%')
        UNDER25 = 'UNDER25', _('Under 25%')

    class DemandSupply(models.TextChoices):
        SHORTAGE = 'Shortage'
        STABLE = 'Stable'
        DECLINING = 'Declining'

    class PropertyValue(models.TextChoices):
        INCREASING = 'Increasing'
        STABLE = 'Stable'
        SLOW = 'Slow'
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=10, blank=True, null=True, choices=Location.choices)
    name = models.CharField(max_length=30, blank=True, null=True)
    built_up = models.CharField(max_length=15, blank=True, null=True, choices=BuiltUp.choices)
    growth_rate = models.CharField(max_length=10, blank=True, null=True, choices=GrowthRate.choices)
    property_value = models.CharField(max_length=15, blank=True, null=True, choices=PropertyValue.choices)
    demand_supply = models.CharField(max_length=20, blank=True, null=True, choices=DemandSupply.choices)
    marketability_factors = models.TextField(blank=True, null=True)
    market_conditions = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, models.DO_NOTHING)
