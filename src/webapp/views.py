from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

from src.WebAppraisal.forms import NewUserForm, UpdateAccountForm, UpdatePhoneNumberForm
from src.webapp.models import Profile

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

def logout_view(request):
    logout(request)
    return redirect('welcome/')

# for new users to create an account
def create_account_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = form.cleaned_data.get('user_role')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
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
    additional_user_info = Profile.objects.get(pk=request.user.id)

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
def app1(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'app1.html', {'user': current_user})


@login_required(login_url='/welcome')
def app2(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'app2.html', {'user': current_user})

@login_required(login_url='/welcome')
def app3(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'app3.html', {'user': current_user})

@login_required(login_url='/welcome')
def app4(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'app4.html', {'user': current_user})

@login_required(login_url='/welcome')
def app5(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'app5.html', {'user': current_user})