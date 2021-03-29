from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from src.WebAppraisal.forms import *
from src.webapp.models import *

@login_required(login_url='/welcome')
def view(request, house_id):
    # TODO: Add generic error page to redirect to when don't have access
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    images = Image.objects.filter(house_id=house_id, page=Image.Pages.MATERIALS_CONDITIONS)

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
                    new_img.page = Image.Pages.MATERIALS_CONDITIONS
                    # set house id
                    new_img.house = House.objects.filter(id=house_id).first()
                    new_img.save()
                    return redirect('/materials-conditions/%s/' % house_id)
                else:
                    return redirect('/materials-conditions/%s/' % house_id)

            elif 'submit_desc' in request.POST:
                img_id = request.POST['img_id']
                img_instance = Image.objects.get(id=img_id)
                form = ImageFormWithDescription(request.POST, instance=img_instance)
                if form.is_valid():
                    form.save()
                    return redirect('/materials-conditions/%s/' % house_id)
                else:
                    return redirect('/materials-conditions/%s/' % house_id)

            # on the button: <input type=submit name=update_account
            if 'submit_materials_condition_info' in request.POST:
                # we need to update the object
                if MaterialsAndCondition.objects.filter(house_id=house_id).exists():
                    materials_conditions_instance = MaterialsAndCondition.objects.get(house_id=house_id)
                    form = MaterialsConditionForm(request.POST, instance=materials_conditions_instance)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "We've successfully updated the materials conditions information")
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
                        messages.success(request, "We've successfully updated the materials conditions information")
                        return redirect('/materials-conditions/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/materials-conditions/%s/' % house_id)

            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/materials-conditions/%s/' % house_id)

        # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
        else:
            img_forms = list(map(lambda img: ImageFormWithDescription(instance=img), images))

            if MaterialsAndCondition.objects.filter(house=house_id).exists():
                materials_conditions_info = MaterialsAndCondition.objects.get(house=house_id)
                form = MaterialsConditionForm(instance=materials_conditions_info)
            else:
                form = MaterialsConditionForm(request.POST)

            return render(request, 'appraisal_edit_forms/materials_conditions.html',
                          context={'form': form, 'house_id': house_id,
                                   'is_mobile': is_mobile, 'mobile_img_form': mobile_img_form,
                                   'img_forms': img_forms, 'new_img_form': add_image_form})
    else:
        if MaterialsAndCondition.objects.filter(house_id=house_id).exists():
            materials_conditions_info = MaterialsAndCondition.objects.get(house_id=house_id)
        else:
            materials_conditions_info = 'empty'
        return render(request, 'customer_view_forms/view_materials_conditions.html',
                      context={'materials_conditions': materials_conditions_info, 'house_id': house_id})
