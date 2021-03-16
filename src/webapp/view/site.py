from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from src.WebAppraisal.forms import *
from src.webapp.models import *

@login_required(login_url='/welcome')
def view(request, house_id):
    role = Profile.objects.get(user_id=request.user.id).role
    images = Image.objects.filter(house_id=house_id, page=Image.Pages.SITE)

    is_mobile = request.user_agent.is_mobile
    add_image_form = NewImageForm(request.POST)
    mobile_img_form = MobileImageForm(request.POST)

    if request.method == 'POST':
        if 'user_logout' in request.POST:
            logout(request)
            redirect('/welcome')
            # on the button: <input type=submit name=update_account

        elif 'img' in request.FILES:
            form = NewImageForm(request.POST, request.FILES)
            if form.is_valid():
                new_img = form.save(commit=False)
                # set page
                new_img.page = Image.Pages.SITE
                # set house id
                new_img.house = House.objects.filter(id=house_id).first()
                new_img.save()
                return redirect('/site/%s/' % house_id)
            else:
                return redirect('/site/%s/' % house_id)

        elif 'submit_desc' in request.POST:
            img_id = request.POST['img_id']
            img_instance = Image.objects.get(id=img_id)
            form = ImageFormWithDescription(request.POST, instance=img_instance)
            if form.is_valid():
                form.save()
                return redirect('/site/%s/' % house_id)
            else:
                return redirect('/site/%s/' % house_id)

        if 'submit_site_info' in request.POST:
            # we need to update the object
            if Site.objects.filter(house_id=house_id).exists():
                site_info = Site.objects.get(house_id=house_id)
                form = SiteForm(request.POST, instance=site_info)

                if form.is_valid():
                    form.save()
                    messages.success(request, "We've successfully updated the site information")
                    return redirect('/site/%s/' % house_id)
                # hopefully won't reach here but just in case redirect back to same page
                else:
                    return redirect('/site/%s/' % house_id)

            # we need to create a new instance
            else:
                form = SiteForm(request.POST)
                if form.is_valid():
                    new_table_instance = form.save(commit=False)
                    # Important: set foreign key to house id
                    new_table_instance.house = House.objects.get(id=house_id)
                    new_table_instance.save()
                    messages.success(request, "We've successfully updated the housing information")
                    return redirect('/site/%s/' % house_id)
                # hopefully won't reach here but just in case redirect back to same page
                else:
                    return redirect('/site/%s/' % house_id)

        # hopefully won't reach here but just in case redirect back to same page
        else:
            return redirect('/site/%s/' % house_id)

    # haven't submitted anything - get blank form if object doesn't exist or create form using existing object
    else:
        img_forms = list(map(lambda img: ImageFormWithDescription(instance=img), images))
        if Site.objects.filter(house=house_id).exists():
            site_info = Site.objects.get(house=house_id)
            form = SiteForm(instance=site_info)
        else:
            form = SiteForm(request.POST)

        return render(request, 'appraisal_edit_forms/site.html', context={'form': form, 'house_id': house_id,
                                                                                              'is_mobile': is_mobile, 'mobile_img_form': mobile_img_form,
                                                                                              'img_forms': img_forms, 'new_img_form': add_image_form })
