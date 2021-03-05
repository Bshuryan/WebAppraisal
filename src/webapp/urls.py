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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from src.webapp import views

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
    path('general/<int:house_id>', views.general_view),
    path('neighborhood/<house_id>', views.neighborhood_view),
    path('site/<house_id>', views.site_view),
    path('description-improvements/<house_id>', views.improvements_view),
    path('comments', views.comment_view),
    path('property-information/<house_id>', views.property_information_view, name='property'),
    path('comments', views.comment_view),
    path('materials-conditions/<house_id>', views.materials_condition_view),
    path('kitchen', views.kitchen_view),
    path('basement', views.basement_view),
    path('utilities', views.utilities_view),
    path('offsite-information', views.offsite_information_view),
    path('AppraisalPage', views.appraisal_view),
    path('amenities', views.amenities_view),
    path('rooms/<house_id>', views.rooms_view),
    path('rooms/<house_id>/add', views.add_room_view),
    path('rooms/<house_id>/<room_id>', views.single_room_view),

    # adding optional slashes
    path('general/new/', views.create_appraisal),
    path('general/<int:house_id>/', views.general_view),
    path('neighborhood/<house_id>/', views.neighborhood_view),
    path('site/<house_id>/', views.site_view),
    path('description-improvements/<house_id>/', views.improvements_view),
    path('comments/', views.comment_view),
    path('property-information/<house_id>/', views.property_information_view),
    path('comments/', views.comment_view),
    path('materials-conditions/<house_id>/', views.materials_condition_view),
    path('kitchen/', views.kitchen_view),
    path('basement/', views.basement_view),
    path('utilities/', views.utilities_view),
    path('offsite-information/', views.offsite_information_view),
    path('AppraisalPage/', views.appraisal_view),
    path('amenities/', views.amenities_view),
    path('rooms/<house_id>/', views.rooms_view),
    path('rooms/<house_id>/add/', views.add_room_view),
    path('rooms/<house_id>/<room_id>/', views.single_room_view)
]
