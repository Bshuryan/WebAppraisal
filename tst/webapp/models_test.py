from django.test import TestCase
from src.webapp.models import Profile
from src.webapp.models import User

class ModelsTest(TestCase):
    def test_get_display_appraiser(self):
        appraiser = Profile.objects.create(user_id=2, phone_number='123-4567', role=Profile.Roles.APPRAISER)
        self.assertEqual(appraiser.get_display_role(), 'Appraiser')
        appraiser.delete()

    def test_get_display_customer(self):
        customer = Profile.objects.create(user_id=3, role=Profile.Roles.CUSTOMER)
        self.assertEqual(customer.get_display_role(), 'Customer requesting appraisal')
        customer.delete()


