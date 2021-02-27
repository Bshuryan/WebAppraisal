from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

from src.WebAppraisal.forms import *
from src.webapp.models import *

APPRAISER_ROLE = 'APPRAISER'
CUSTOMER_ROLE = 'CUSTOMER'

# empty url - redirect user to login/welcome page
def redirect_to_login(request):
    return redirect('/welcome/')

# login page - default when first opening the webapp
def login_view(request):
    logout(request)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            clean_usn = form.cleaned_data['username']
            clean_pswd = form.cleaned_data['password']
            user = authenticate(username=clean_usn, password=clean_pswd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/home")
                else:
                    return render(request, 'loginpage.html', {'form': form })
        else:
            pass
    else:
        form = AuthenticationForm()
    return render(request, "loginpage.html", {"form": form })

# for new users to create an account
def create_account_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_id = User.objects.get(username=user.username).id
            profile = Profile.objects.create(phone_number=form.cleaned_data.get('phone_number'),
                                             role=form.cleaned_data.get('user_role'),
                                             user_id=user_id)
            user.profile = profile
            user.save()
            raw_password = form.cleaned_data.get('password1')
            usr = authenticate(username=user.username, password=raw_password)
            login(request, usr)
            return redirect('/home/')
    else:
        form = NewUserForm()
    return render(request, 'sign-up.html', {'form': form})

# home page for both appraisers and their customers
@login_required(login_url='/welcome')
def dashboard_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'homepage.html', {'user': current_user})

# view where users can change their account information or delete their account
@login_required(login_url='/welcome')
def account_management_view(request):
    user = User.objects.get(pk=request.user.id)
    additional_user_info = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        # on the button: <input type=submit name=update_account
        if 'update_account' in request.POST:
            user_form = UpdateAccountForm(request.POST, instance=user)
            phone_num_form = UpdatePhoneNumberForm(request.POST, instance=additional_user_info)

            if user_form.is_valid() or phone_num_form.is_valid():
                if user_form.is_valid():
                    user_form.save()

                if phone_num_form.is_valid():
                    phone_num_form.save()
                # see https://stackoverflow.com/questions/28723266/django-display-message-after-post-form-submit to implement
                messages.success(request, "We've successfully updated your account")
                return redirect('/account-management')
            else:
                return redirect('/account-management')

        elif 'delete_account_confirm' in request.POST:
            user.delete()
            return redirect('/welcome')

        else:
            return redirect('/account-management')

    else:
        user_form = UpdateAccountForm(instance=user)
        phone_num_form = UpdatePhoneNumberForm(instance=additional_user_info)
        return render(request, 'manage-account.html', context={'user_form': user_form, 'phone_num_form': phone_num_form,
                                                             'django_user': user, 'webappraisal_user': additional_user_info,
                                                             'role': additional_user_info.get_display_role() })




@login_required(login_url='/welcome')
def general_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/general.html', {'user': current_user})


@login_required(login_url='/welcome')
def neighborhood_view(request, house_id):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')
            # on the button: <input type=submit name=update_account
        if 'submit_neighborhood_info' in request.POST:
            # we need to update the object
            if Neighborhood.objects.filter(house_id=house_id).exists():
                neighborhood_info = Neighborhood.objects.get(house_id=house_id)
                form = NeighborhoodForm(request.POST, instance=neighborhood_info)

                if form.is_valid():
                    form.save()
                    messages.success(request, "We've successfully updated the neighborhood information")
                    return redirect('/neighborhood/%s/' % house_id)
                # hopefully won't reach here but just in case redirect back to same page
                else:
                    return redirect('/neighborhood/%s/' % house_id)

            # we need to create a new instance
            else:
                form = NeighborhoodForm(request.POST)
                if form.is_valid():
                    new_table_instance = form.save(commit=False)
                    # Important: set foreign key to house id
                    new_table_instance.house = House.objects.get(id=house_id)
                    new_table_instance.save()
                    messages.success(request, "We've successfully updated the housing information")
                    return redirect('/neighborhood/%s/' % house_id)
                # hopefully won't reach here but just in case redirect back to same page
                else:
                    return redirect('/neighborhood/%s/' % house_id)

        # hopefully won't reach here but just in case redirect back to same page
        else:
            return redirect('/neighborhood/%s/' % house_id)

    # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
    else:
        if Neighborhood.objects.filter(house=house_id).exists():
            neighborhood_info = Neighborhood.objects.get(house=house_id)
            form = NeighborhoodForm(instance=neighborhood_info)
        else:
            form = NeighborhoodForm(request.POST)

        return render(request, 'appraisal_edit_forms/neighborhood.html', context={'form': form})

@login_required(login_url='/welcome')
def site_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/site.html', {'user': current_user})

@login_required(login_url='/welcome')
def improvements_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')
    return render(request, 'appraisal_edit_forms/description_improvements.html', {'user': current_user})

@login_required(login_url='/welcome')
def comment_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/comments.html', {'user': current_user})

@login_required(login_url='/welcome')
def property_information_view(request, house_id):
    # TODO: Add generic error page to redirect to when don't have access
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    if request.method == 'POST':
        # shared logic among views for user logout
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

        # on the button: <input type=submit name=update_account
        if 'submit_prop_info' in request.POST:
            # we need to update the object
            if Property.objects.filter(house_id=house_id).exists():
                property_info = Property.objects.get(house_id=house_id)
                form = PropertyInformationForm(request.POST, instance=property_info)

                if form.is_valid():
                    form.save()
                    messages.success(request, "We've successfully updated the housing information")
                    return redirect('/property-information/%s/' % house_id)
                # hopefully won't reach here but just in case redirect back to same page
                else:
                    return redirect('/property-information/%s/' % house_id)

            # we need to create a new instance
            else:
                form = PropertyInformationForm(request.POST)
                if form.is_valid():
                    new_table_instance = form.save(commit=False)
                    # Important: set foreign key to house id
                    new_table_instance.house = House.objects.get(id=house_id)
                    new_table_instance.save()
                    messages.success(request, "We've successfully updated the housing information")
                    return redirect('/property-information/%s/' % house_id)
                # hopefully won't reach here but just in case redirect back to same page
                else:
                    return redirect('/property-information/%s/' % house_id)

        # hopefully won't reach here but just in case redirect back to same page
        else:
            return redirect('/property-information/%s/' % house_id)

    # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
    else:
        if Property.objects.filter(house=house_id).exists():
            property_info = Property.objects.get(house=house_id)
            form = PropertyInformationForm(instance=property_info)
        else:
            form = PropertyInformationForm(request.POST)

        return render(request, 'appraisal_edit_forms/property_information.html', context={'form': form })

@login_required(login_url='/welcome')
def materials_conditions_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')
    return render(request, 'appraisal_edit_forms/materials_conditions.html', {'user': current_user})

@login_required(login_url='/welcome')
def kitchen_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/kitchen.html', {'user': current_user})

@login_required(login_url='/welcome')
def basement_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/basement.html', {'user': current_user})

@login_required(login_url='/welcome')
def utilities_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/utilities.html', {'user': current_user})


@login_required(login_url='/welcome')
def offsite_information_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/offsite_information.html', {'user': current_user})

@login_required(login_url='/welcome')
def appraisal_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/AppraisalPage.html', {'user': current_user})


@login_required(login_url='/welcome')
def amenities_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/amenities.html', {'user': current_user})

@login_required(login_url='/welcome')
def sitero_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'customer_view_forms/view_site.html', {'user': current_user})
