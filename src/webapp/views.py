from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.defaulttags import register

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
    role = Profile.objects.get(user_id=request.user.id).role
    images = {}
    if request.method == 'POST':

        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

        elif 'img' in request.FILES:
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                house_id = form.cleaned_data['house'].id
                # remove old instance so previous photos won't show up
                Image.objects.filter(house_id=house_id).delete()
                new_img = form.save(commit=False)
                # set page
                new_img.page = Image.Pages.HOME
                # set house id
                current_house = form.cleaned_data['house']
                new_img.house = current_house
                new_img.save()

                return redirect('/home')
            else:
                return redirect('/home')
        else:
            return redirect('/home')

    if role == Profile.Roles.APPRAISER:
        form = ImageForm()
        houses = list(House.objects.filter(appraiser=current_user))
        for house in houses:
            if Image.objects.filter(page=Image.Pages.HOME, house_id=house.id).exists():
                images[house.id] = Image.objects.filter(page=Image.Pages.HOME, house_id=house.id).first()
            else:
                images[house.id] = None

    else:
        form = ImageForm()
        houses = list(House.objects.filter(customer=current_user))
        for house in houses:
            if Image.objects.filter(page=Image.Pages.HOME, house_id=house.id).exists():
                images[house.id] = Image.objects.filter(page=Image.Pages.HOME, house_id=house.id).first()
            else:
                images[house.id] = None

    return render(request, 'homepage.html', {'user': current_user, 'role': role.__str__(), 'houses': houses,
                                             'images': images, 'form': form})

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
def create_appraisal(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

        if 'submit_general_info' in request.POST:
            form = CreateAppraisalForm(request.POST)
            if form.is_valid():
                new_house = form.save(commit=False)
                customer_username = form.cleaned_data.get('customer_username')
                new_house.customer = User.objects.filter(username=customer_username).first()
                new_house.appraiser = current_user
                new_house.save()
                messages.success(request, "We've successfully updated the housing information")
                house_id = new_house.id
                request.session['is_created'] = 1
                # request.session['is_updated'] = 0
                request.session.modified = True
                return redirect('/general/' + str(house_id))
            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/general/new')
        else:
            return redirect('/general/new')

    # haven't submitted anything - get blank form
    else:
        form = CreateAppraisalForm()
        return render(request, 'appraisal_edit_forms/create_appraisal.html', context={'form': form, 'appraiser': current_user})

@login_required(login_url='/welcome')
def improvements_view(request, house_id):
    # TODO: Add generic error page to redirect to when don't have access
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    if role == Profile.Roles.APPRAISER:
        if request.method == 'POST':
            # shared logic among views for user logout
            if 'user_logout' in request.POST:
                logout(request)
                redirect('/welcome')

            # on the button: <input type=submit name=update_account
            if 'submit_improvements_info' in request.POST:
                # we need to update the object
                if DescriptionOfImprovements.objects.filter(house_id=house_id).exists():
                    improvements_info = DescriptionOfImprovements.objects.get(house_id=house_id)
                    form = DescriptionOfImprovementsForm(request.POST, instance=improvements_info)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "We've successfully updated the improvements information")
                        return redirect('/description-improvements/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/description-improvements/%s/' % house_id)

                # we need to create a new instance
                else:
                    form = DescriptionOfImprovementsForm(request.POST)
                    if form.is_valid():
                        new_table_instance = form.save(commit=False)
                        # Important: set foreign key to house id
                        new_table_instance.house = House.objects.get(id=house_id)
                        new_table_instance.save()
                        messages.success(request, "We've successfully updated the housing information")
                        return redirect('/description-improvements/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/description-improvements/%s/' % house_id)

            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/description-improvements/%s/' % house_id)

        # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
        else:
            if DescriptionOfImprovements.objects.filter(house=house_id).exists():
                improvements_info = DescriptionOfImprovements.objects.get(house=house_id)
                form = DescriptionOfImprovementsForm(instance=improvements_info)
            else:
                form = DescriptionOfImprovementsForm(request.POST)

            return render(request, 'appraisal_edit_forms/description_improvements.html',
                          context={'form': form, 'house_id': house_id})
    else:
        if DescriptionOfImprovements.objects.filter(house_id=house_id).exists():
            improvements_info = DescriptionOfImprovements.objects.get(house_id=house_id)
        else:
            improvements_info = 'empty'
        return render(request, 'customer_view_forms/view_description_improvements.html',
                      context={'improvements': improvements_info, 'house_id': house_id})

@login_required(login_url='/welcome')
def comment_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'appraisal_edit_forms/comments.html', {'user': current_user})


@login_required(login_url='/welcome')
def materials_condition_view(request, house_id):
    # TODO: Add generic error page to redirect to when don't have access
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    if role == Profile.Roles.APPRAISER:
        if request.method == 'POST':
            # shared logic among views for user logout
            if 'user_logout' in request.POST:
                logout(request)
                redirect('/welcome')

            # on the button: <input type=submit name=update_account
            if 'submit_materials_condition_info' in request.POST:
                # we need to update the object
                if MaterialsAndCondition.objects.filter(house_id=house_id).exists():
                    materials_condition_info = MaterialsAndCondition.objects.get(house_id=house_id)
                    form = MaterialsConditionForm(request.POST, instance=materials_condition_info)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "We've successfully updated the materials and conditions information")
                        return redirect('/materials-conditions/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/materials-conditions/%s/' % house_id)

                # we need to create a new instance
                else:
                    form = MaterialsConditionForm(request.POST)
                    if form.is_valid():
                        new_table_instance = form.save(commit=False)
                        # Important: set foreign key to house id
                        new_table_instance.house = House.objects.get(id=house_id)
                        new_table_instance.save()
                        messages.success(request, "We've successfully updated the housing information")
                        return redirect('/materials-conditions/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/materials-conditions/%s/' % house_id)

            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/materials-conditions/%s/' % house_id)

        # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
        else:
            if MaterialsAndCondition.objects.filter(house=house_id).exists():
                materials_condition_info = MaterialsAndCondition.objects.get(house=house_id)
                form = MaterialsConditionForm(instance=materials_condition_info)
            else:
                form = MaterialsConditionForm(request.POST)

            return render(request, 'appraisal_edit_forms/materials_conditions.html',
                          context={'form': form, 'house_id': house_id})
    else:
        if MaterialsAndCondition.objects.filter(house_id=house_id).exists():
            materials_condition_info = MaterialsAndCondition.objects.get(house_id=house_id)
        else:
            materials_condition_info = 'empty'
        return render(request, 'customer_view_forms/view_materials_conditions.html',
                      context={'materials_condition': materials_condition_info, 'house_id': house_id})



@login_required(login_url='/welcome')
def amenities_view(request, house_id):
    # TODO: Add generic error page to redirect to when don't have access
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    if role == Profile.Roles.APPRAISER:
        if request.method == 'POST':
            # shared logic among views for user logout
            if 'user_logout' in request.POST:
                logout(request)
                redirect('/welcome')

            # on the button: <input type=submit name=update_account
            if 'submit_amenities_info' in request.POST:
                # we need to update the object
                if Amenities.objects.filter(house_id=house_id).exists():
                    amenities_info = Amenities.objects.get(house_id=house_id)
                    form = AmenitiesForm(request.POST, instance=amenities_info)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "We've successfully updated the amenities information")
                        return redirect('/amenities/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/amenities/%s/' % house_id)

                # we need to create a new instance
                else:
                    form = AmenitiesForm(request.POST)
                    if form.is_valid():
                        new_table_instance = form.save(commit=False)
                        # Important: set foreign key to house id
                        new_table_instance.house = House.objects.get(id=house_id)
                        new_table_instance.save()
                        messages.success(request, "We've successfully updated the housing information")
                        return redirect('/amenities/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/amenities/%s/' % house_id)

            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/amenities/%s/' % house_id)

        # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
        else:
            if Amenities.objects.filter(house=house_id).exists():
                amenities_info = Amenities.objects.get(house=house_id)
                form = AmenitiesForm(instance=amenities_info)
            else:
                form = AmenitiesForm(request.POST)

            return render(request, 'appraisal_edit_forms/amenities.html',
                          context={'form': form, 'house_id': house_id})
    else:
        if Amenities.objects.filter(house_id=house_id).exists():
            amenities_info = Amenities.objects.get(house_id=house_id)
        else:
            amenities_info = 'empty'
        return render(request, 'customer_view_forms/view_amenities.html',
                      context={'improvements': amenities_info, 'house_id': house_id})

@login_required(login_url='/welcome')
def sitero_view(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

    return render(request, 'customer_view_forms/view_site.html', {'user': current_user})


@login_required(login_url='/welcome')
def rooms_view(request, house_id):
    rooms = list(Room.objects.filter(house=house_id))
    # TODO: Add generic error page to redirect to when don't have access
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    if role == Profile.Roles.APPRAISER:
        if request.method == 'POST':
            # shared logic among views for user logout
            if 'user_logout' in request.POST:
                logout(request)
                redirect('/welcome')

            # on the button: <input type=submit name=update_account
            if 'submit_rooms_summary' in request.POST:
                # we need to update the object
                if RoomSummary.objects.filter(house_id=house_id).exists():
                    summary = RoomSummary.objects.get(house_id=house_id)
                    form = RoomsForm(request.POST, instance=summary)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "We've successfully updated the housing information")
                        return redirect('/rooms/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/rooms/%s/' % house_id)

                # we need to create a new instance
                else:
                    form = RoomsForm(request.POST)
                    if form.is_valid():
                        new_table_instance = form.save(commit=False)
                        # Important: set foreign key to house id
                        new_table_instance.house = House.objects.get(id=house_id)
                        new_table_instance.save()
                        messages.success(request, "We've successfully updated the housing information")
                        return redirect('/rooms/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/rooms/%s/' % house_id)

            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/rooms/%s/' % house_id)

        # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
        else:
            if RoomSummary.objects.filter(house=house_id).exists():
                summary = RoomSummary.objects.get(house=house_id)
                form = RoomsForm(instance=summary)
            else:
                form = RoomsForm()

            return render(request, 'appraisal_edit_forms/rooms.html',
                          context={'form': form, 'house_id': house_id,
                                   'rooms': rooms})
    # where customer view will go
    else:
        if RoomSummary.objects.filter(house_id=house_id).exists():
            summary = RoomSummary.objects.get(house_id=house_id)
        else:
            summary = 'empty'
        return render(request, 'customer_view_forms/view_rooms.html', context={'summary': summary, 'rooms': rooms })


@login_required(login_url='/welcome')
def add_room_view(request, house_id):
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

        if 'submit_room' in request.POST:
            form = AddRoomForm(request.POST)
            if form.is_valid():
                new_room = form.save(commit=False)
                new_room.house = House.objects.filter(id=house_id).first()
                new_room.save()
                messages.success(request, "We've successfully updated the housing information")
                return redirect('/rooms/' + str(house_id))
            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/rooms/' + str(house_id) + '/add')
        else:
            return redirect('/rooms/' + str(house_id) + '/add')

    # haven't submitted anything - get blank form
    else:
        form = AddRoomForm()
        return render(request, 'appraisal_edit_forms/add_room.html',
                      context={'form': form})


@login_required(login_url='/welcome')
def single_room_view(request, house_id, room_id):
    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')

        if 'submit_room' in request.POST:
            if Room.objects.filter(id=room_id).exists():
                existing_room = Room.objects.get(id=room_id)
                form = EditRoomForm(request.POST, instance=existing_room)
                if form.is_valid():
                    form.save()
                    messages.success(request, "We've successfully updated the housing information")
                    return redirect('/rooms/' + str(house_id))
                # hopefully won't reach here but just in case redirect back to same page
                else:
                    return redirect('/rooms/' + str(house_id))
            else:
                return redirect('/rooms/' + str(house_id))
        else:
            return redirect('/rooms/' + str(house_id))

    # haven't submitted anything - get blank form
    else:
        if Room.objects.filter(id=room_id).exists():
            existing_room = Room.objects.get(id=room_id)
            form = EditRoomForm(instance=existing_room)
        else:
            return redirect('/rooms/' + str(house_id))

        return render(request, 'appraisal_edit_forms/edit_room.html',
                      context={'form': form})


@register.filter
def get_item(dictionary, key):
    # print('filter values')
    # print(str(key) + str(dictionary.get(key)))
    return dictionary.get(key)

@register.filter
def set_item(dictionary, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    key = arg_list[0]
    value = arg_list[1]
    dictionary[key] = value
    return ""
