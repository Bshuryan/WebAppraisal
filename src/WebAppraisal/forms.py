from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from src.webapp.models import *

# Form for creating a new user - this includes all fields for the built-in Django User object
# and three additional fields on top of it: email, phone number, and user role
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    user_role = forms.ChoiceField(required=True, choices=Profile.Roles.choices)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "phone_number", "user_role")

# Form for updating the built-in Django User object
class UpdateAccountForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

# form for updating a user's phone number
# this is separate from the other update user account form because phone number is not
# a field supported by the Django User object type
class UpdatePhoneNumberForm(forms.ModelForm):
    phone_number = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ["phone_number"]

    def save(self, commit=True):
        user = super(UpdatePhoneNumberForm, self).save(commit=False)

        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user

class PropertyInformationForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['house', 'id']

class NeighborhoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        exclude = ['house', 'id']

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        exclude = ['house', 'id']

class DescriptionOfImprovementsForm:
    class Meta:
        model = DescriptionOfImprovements
        exclude = ['house', 'id']

class MaterialsConditionForm(forms.ModelForm):
    class Meta:
        model = MaterialsAndCondition
        exclude = ['house', 'id']

class CreateAppraisalForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['street_address', 'city', 'state', 'zip', 'county', 'appraisal_status', 'comments']

    def __init__(self, *args, **kwargs):
        super(CreateAppraisalForm, self).__init__(*args, **kwargs)
        self.fields['customer_username'] = forms.CharField(max_length=50)


class UpdateAppraisalForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ['customer', 'appraiser', 'id']
