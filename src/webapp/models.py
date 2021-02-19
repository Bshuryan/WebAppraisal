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
class Appraisal(models.Model):
    id = models.IntegerField(primary_key=True)
    house_id = models.IntegerField()
    positive_features = models.TextField(blank=True, null=True)
    negative_conditions = models.TextField(blank=True, null=True)
    reconciliation = models.TextField(blank=True, null=True)
    appraisal_price = models.IntegerField(blank=True, null=True)