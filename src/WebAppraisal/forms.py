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

class DescriptionOfImprovementsForm(forms.ModelForm):
    class Meta:
        model = DescriptionOfImprovements
        exclude = ['house', 'id']

class MaterialsConditionForm(forms.ModelForm):
    class Meta:
        model = MaterialsAndCondition
        exclude = ['house', 'id']

class BasementForm(forms.ModelForm):
    class Meta:
        model = Basement
        exclude = ['house', 'id']

class KitchenForm(forms.ModelForm):
    class Meta:
        model = Kitchen
        exclude = ['house', 'id']

class OffsiteForm(forms.ModelForm):
    class Meta:
        model = Offsite
        exclude = ['house', 'id']

class UtilitiesForm(forms.ModelForm):
    class Meta:
        model = Utilities
        exclude = ['house', 'id']

class FoundationForm(forms.ModelForm):
    class Meta:
        model = Foundation
        exclude = ['house', 'id']

class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        exclude = ['house', 'id']

class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
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

class RoomsForm(forms.ModelForm):
    class Meta:
        model = RoomSummary
        exclude = ['id', 'house']

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['id', 'house']

class EditRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['id', 'house']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img', 'house']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['img'].widget.attrs.update({'name': 'change_img',
                                                'id': 'change_img',
                                                'style': 'display: none;',
                                                'onchange': 'this.form.submit();'})

class ImageFormWithDescription(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['description', 'id']

    def __init__(self, *args, **kwargs):
        super(ImageFormWithDescription, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'style': 'height: 50%;',
                                                        'onchange': 'this.form.submit();'})

class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img']

    def __init__(self, *args, **kwargs):
        super(NewImageForm, self).__init__(*args, **kwargs)
        self.fields['img'].widget.attrs.update({'name': 'change_img',
                                                'id': 'change_img',
                                                'style': 'display: none;',
                                                'onchange': 'this.form.submit();'})

class MobileImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img']

    def __init__(self, *args, **kwargs):
        super(MobileImageForm, self).__init__(*args, **kwargs)
        self.fields['img'].widget.attrs.update({'name': 'change_img',
                                                'id': 'change_img',
                                                'style': 'display: none;',
                                                'capture': 'environment',
                                                'accepts': 'image/',
                                                'onchange': 'this.form.submit();'})

