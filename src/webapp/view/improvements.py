from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from src.WebAppraisal.forms import *
from src.webapp.models import *

@login_required(login_url='/welcome')
def view(request, house_id):
    # assert hasAccessToAppraisal(user_id=request.user.id, house_id=house_id) is True
    role = Profile.objects.get(user_id=request.user.id).role
    images = Image.objects.filter(house_id=house_id, page=Image.Pages.DESC_IMPROV)

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
                    new_img.page = Image.Pages.DESC_IMPROV
                    # set house id
                    new_img.house = House.objects.filter(id=house_id).first()
                    new_img.save()
                    return redirect('/description_improvements/%s/' % house_id)
                else:
                    return redirect('/description_improvements/%s/' % house_id)

            elif 'submit_desc' in request.POST:
                img_id = request.POST['img_id']
                img_instance = Image.objects.get(id=img_id)
                form = ImageFormWithDescription(request.POST, instance=img_instance)
                if form.is_valid():
                    form.save()
                    return redirect('/description_improvements/%s/' % house_id)
                else:
                    return redirect('/description_improvements/%s/' % house_id)

            # on the button: <input type=submit name=update_account
            if 'submit_improvements_info' in request.POST:
                # we need to update the object
                if DescriptionOfImprovements.objects.filter(house_id=house_id).exists():
                    improvements_info = DescriptionOfImprovements.objects.get(house_id=house_id)
                    form = DescriptionOfImprovementsForm(request.POST, instance=improvements_info)

                    if form.is_valid():
                        form.save()
                        messages.success(request, "We've successfully updated the improvements information")
                        return redirect('/description_improvements/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/description_improvements/%s/' % house_id)

                # we need to create a new instance
                else:
                    form = DescriptionOfImprovementsForm(request.POST)
                    if form.is_valid():
                        new_table_instance = form.save(commit=False)
                        # Important: set foreign key to house id
                        new_table_instance.house = House.objects.get(id=house_id)
                        new_table_instance.save()
                        messages.success(request, "We've successfully updated the improvements information")
                        return redirect('/description_improvements/%s/' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/description_improvements/%s/' % house_id)

            # hopefully won't reach here but just in case redirect back to same page
            else:
                return redirect('/description_improvements/%s/' % house_id)

        # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
        else:
            img_forms = list(map(lambda img: ImageFormWithDescription(instance=img), images))

            if DescriptionOfImprovements.objects.filter(house=house_id).exists():
                improvements_info = DescriptionOfImprovements.objects.get(house=house_id)
                form = DescriptionOfImprovementsForm(instance=improvements_info)
            else:
                form = DescriptionOfImprovementsForm(request.POST)

            return render(request, 'appraisal_edit_forms/description_improvements.html',
                          context={'form': form, 'house_id': house_id,
                                   'is_mobile': is_mobile, 'mobile_img_form': mobile_img_form,
                                   'img_forms': img_forms, 'new_img_form': add_image_form})
    else:
        if DescriptionOfImprovements.objects.filter(house_id=house_id).exists():
            improvements_info = DescriptionOfImprovements.objects.get(house_id=house_id)
        else:
            improvements_info = 'empty'
        return render(request, 'customer_view_forms/view_description_improvements.html',
                      context={'improvements': improvements_info, 'house_id': house_id})
