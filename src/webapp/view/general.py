from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from src.WebAppraisal.forms import *
from src.webapp.models import *


@login_required(login_url='/welcome')
def view(request, house_id):
    user_role = Profile.objects.get(user_id=request.user.id).role
    house_instance = House.objects.get(id=house_id)
    images = Image.objects.filter(house_id=house_id, page=Image.Pages.GENERAL)
    if user_role == Profile.Roles.APPRAISER:
        is_mobile = request.user_agent.is_mobile
        add_image_form = NewImageForm(request.POST)
        mobile_img_form = MobileImageForm(request.POST)
        if not House.objects.filter(id=house_id).exists():
            redirect('/general/new')
        else:
            if request.method == 'POST':

                if 'user_logout' in request.POST:
                    logout(request)
                    redirect('/welcome')

                elif 'img' in request.FILES:
                    form = NewImageForm(request.POST, request.FILES)
                    if form.is_valid():
                        new_img = form.save(commit=False)
                        # set page
                        new_img.page = Image.Pages.GENERAL
                        # set house id
                        new_img.house = House.objects.filter(id=house_id).first()
                        new_img.save()
                        request.session['is_created'] = 0
                        request.session['is_updated'] = 1
                        request.session.modified = True
                        return redirect('/general/%s' % house_id)
                    else:
                        return redirect('/general/%s' % house_id)

                elif 'submit_desc' in request.POST:
                    img_id = request.POST['img_id']
                    img_instance = Image.objects.get(id=img_id)
                    form = ImageFormWithDescription(request.POST, instance=img_instance)
                    if form.is_valid():
                        form.save()
                        request.session['is_created'] = 0
                        request.session['is_updated'] = 1
                        request.session.modified = True
                        return redirect('/general/%s' % house_id)
                    else:
                        return redirect('/general/%s' % house_id)

                elif 'submit_general_info' in request.POST:
                    form = UpdateAppraisalForm(request.POST, instance=house_instance)
                    if form.is_valid():
                        form.save()
                        request.session['is_created'] = 0
                        request.session['is_updated'] = 1

                        request.session.modified = True
                        return redirect('/general/%s' % house_id)
                    # hopefully won't reach here but just in case redirect back to same page
                    else:
                        return redirect('/general/%s' % house_id)
                else:
                    return redirect('/general/%s' % house_id)
            # render form using existing info
            else:
                form = UpdateAppraisalForm(instance=house_instance)
                img_forms = list(map(lambda img: ImageFormWithDescription(instance=img), images))
                phone_num = Profile.objects.get(user_id=house_instance.customer.id).phone_number
                if not phone_num:
                    phone_num = 'Not entered'

                # request.session['is_updated'] = 0
                request.session.modified = True

                return render(request, 'appraisal_edit_forms/general.html', {'customer': house_instance.customer,
                                                                             'form': form, 'phone_number': phone_num,
                                                                             'house_id': house_id, 'role': user_role,
                                                                             'img_forms': img_forms, 'new_img_form': add_image_form,
                                                                             'is_mobile': is_mobile, 'mobile_img_form': mobile_img_form })
    # user is a customer
    else:
        phone_num = Profile.objects.get(user_id=house_instance.appraiser.id).phone_number
        return render(request, 'customer_view_forms/view_general.html', context={'appraiser': house_instance.appraiser,
                                                                                 'house': house_instance, 'house_id': house_id,
                                                                                 'phone_number': phone_num, 'images': images,
                                                                                 'role': user_role})