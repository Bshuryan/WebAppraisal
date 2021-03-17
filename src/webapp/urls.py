"""WebAppraisal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from src.webapp import views
from src.webapp.view import general
from src.webapp.view import property_information
from src.webapp.view import neighborhood
from src.webapp.view import site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_login),
    path('accounts/', include('django.contrib.auth.urls')),
    path('welcome/', views.login_view),
    path('create-account/', views.create_account_view),
    path('home/', views.dashboard_view),
    path('account-management/', views.account_management_view),

    # Appraisal paths
    path('general/new', views.create_appraisal),
    path('general/<int:house_id>', general.view),
    path('neighborhood/<house_id>', neighborhood.view),
    path('site/<house_id>', site.view),
    path('description-improvements/<house_id>', views.improvements_view),
    path('comments/<house_id>', views.comment_view),
    path('property-information/<house_id>', property_information.view),
    path('comments', views.comment_view),
    path('materials-conditions/<house_id>', views.materials_condition_view),
    path('kitchen/<house_id>', views.kitchen_view),
    path('basement/<house_id>', views.basement_view),
    path('utilities/<house_id>', views.utilities_view),
    path('foundation/<house_id>',views.foundation_view),
    path('offsite-information/<house_id>', views.offsite_information_view),
    path('AppraisalPage/<house_id>', views.appraisal_view),
    path('amenities/<house_id>', views.amenities_view),
    path('rooms/<house_id>', views.rooms_view),
    path('rooms/<house_id>/add', views.add_room_view),
    path('rooms/<house_id>/<room_id>', views.single_room_view),


    # adding optional slashes
    path('general/new/', views.create_appraisal),
    path('general/<int:house_id>/', general.view),
    path('neighborhood/<house_id>/', neighborhood.view),
    path('site/<house_id>/', site.view),
    path('description-improvements/<house_id>/', views.improvements_view),
    path('comments/<house_id>/', views.comment_view),
    path('property-information/<house_id>/', property_information.view),
    path('materials-conditions/<house_id>/', views.materials_condition_view),
    path('kitchen/<house_id>/', views.kitchen_view),
    path('basement/<house_id>/', views.basement_view),
    path('utilities/<house_id>/', views.utilities_view),
    path('foundation/<house_id>/', views.foundation_view),
    path('offsite-information/<house_id>/', views.offsite_information_view),
    path('AppraisalPage/<house_id>/', views.appraisal_view),
    path('amenities/<house_id>/', views.amenities_view),
    path('rooms/<house_id>/', views.rooms_view),
    path('rooms/<house_id>/add/', views.add_room_view),
    path('rooms/<house_id>/<room_id>/', views.single_room_view)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
