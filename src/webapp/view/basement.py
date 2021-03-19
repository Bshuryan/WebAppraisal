from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from src.WebAppraisal.forms import *
from src.webapp.models import *



@login_required(login_url='/welcome')
def view(request, house_id):
    house_instance = House.objects.filter(id=house_id).first()
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    if role == Profile.Roles.APPRAISER:
        if request.method == 'POST':
            # shared logic among views for user logout
            if 'user_logout' in request.POST:
                logout(request)
                redirect('/welcome')

            # on the button: <input type=submit name=update_account
            if 'submit_basement_info' in request.POST:
                # we need to update the object
                if Basement.objects.filter(house=house_instance).exists():
                    basement_info = Basement.objects.get(house=house_instance)
                    form = BasementForm(request.POST, instance=basement_info)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "We've successfully updated the basement information")
                        return redirect('/basement/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/basement/%s/' % house_id)

                # we need to create a new instance
                else:
                    form = BasementForm(request.POST)
                    if form.is_valid():
                        new_table_instance = form.save(commit=False)
                        # Important: set foreign key to house id
                        new_table_instance.house = House.objects.get(id=house_id)
                        new_table_instance.save()
                        messages.success(request, "We've successfully updated the basement information")
                        return redirect('/basement/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/basement/%s/' % house_id)

            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/basement/%s/' % house_id)

        # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
        else:
            if Basement.objects.filter(house=house_instance).exists():
                basement_info = Basement.objects.get(house=house_instance)
                form = BasementForm(instance=basement_info)
            else:
                form = BasementForm(request.POST)

            return render(request, 'appraisal_edit_forms/basement.html',
                          context={'form': form, 'house_id': house_id})
    else:
        if Basement.objects.filter(house_id=house_id).exists():
            basement_info = Basement.objects.get(house_id=house_id)
        else:
            basement_info = 'empty'
        return render(request, 'customer_view_forms/view_basement.html',
                      context={'basement': basement_info, 'house_id': house_id})