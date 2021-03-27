from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from src.WebAppraisal.forms import *
from src.webapp.models import *

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


@login_required(login_url='/welcome')
def rooms_view(request, house_id):
    rooms = list(Room.objects.filter(house=house_id))
    images = Image.objects.filter(house_id=house_id, page=Image.Pages.ROOMS)

    # TODO: Add generic error page to redirect to when don't have access
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    if role == Profile.Roles.APPRAISER:
        is_mobile = request.user_agent.is_mobile
        add_image_form = NewImageForm(request.POST)
        mobile_img_form = MobileImageForm(request.POST)

        if request.method == 'POST':
            # shared logic among views for user logout
            if 'user_logout' in request.POST:
                logout(request)
                redirect('/welcome')

            elif 'img' in request.FILES:
                form = NewImageForm(request.POST, request.FILES)
                if form.is_valid():
                    new_img = form.save(commit=False)
                    # set page
                    new_img.page = Image.Pages.ROOMS
                    # set house id
                    new_img.house = House.objects.filter(id=house_id).first()
                    new_img.save()
                    return redirect('/rooms/%s/' % house_id)
                else:
                    return redirect('/rooms/%s/' % house_id)

            elif 'submit_desc' in request.POST:
                img_id = request.POST['img_id']
                img_instance = Image.objects.get(id=img_id)
                form = ImageFormWithDescription(request.POST, instance=img_instance)
                if form.is_valid():
                    form.save()
                    return redirect('/rooms/%s/' % house_id)
                else:
                    return redirect('/rooms/%s/' % house_id)

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
            img_forms = list(map(lambda img: ImageFormWithDescription(instance=img), images))
            if RoomSummary.objects.filter(house=house_id).exists():
                summary = RoomSummary.objects.get(house=house_id)
                form = RoomsForm(instance=summary)
            else:
                form = RoomsForm()

            return render(request, 'appraisal_edit_forms/rooms.html',
                          context={'form': form, 'house_id': house_id,
                                   'rooms': rooms, 'is_mobile': is_mobile, 'mobile_img_form': mobile_img_form,
                                    'img_forms': img_forms, 'new_img_form': add_image_form })
    # where customer view will go
    else:
        if RoomSummary.objects.filter(house_id=house_id).exists():
            summary = RoomSummary.objects.get(house_id=house_id)
        else:
            summary = 'empty'
        return render(request, 'customer_view_forms/view_rooms.html', context={'summary': summary, 'rooms': rooms,
                                                                               'house_id': house_id })


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