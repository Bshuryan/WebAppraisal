from django.contrib.auth.models import User
from django.test import TestCase
from src.webapp.models import Profile

class ModelsTest(TestCase):
    def test_get_display_appraiser(self):
        user = User.objects.create(username='ut_appraiser', email='appraiser@gmail.com', password='password')
        appraiser = Profile.objects.create(user_id=user.id, phone_number='123-4567', role=Profile.Roles.APPRAISER)
        self.assertEqual(appraiser.get_display_role(), 'Appraiser')

    def test_get_display_customer(self):
        user = User.objects.create(username='ut_customer', email='customer@gmail.com', password='password')
        customer = Profile.objects.create(user_id=user.id, role=Profile.Roles.CUSTOMER)
        self.assertEqual(customer.get_display_role(), 'Customer requesting appraisal')
        customer.delete()


