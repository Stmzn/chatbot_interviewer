from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import PersonalDetailsView

app_name = 'interview'

urlpatterns = [
    path('', views.load_homepage,name = 'home'),
    path('foo/', views.personalform,name = 'personaldetails'),
    path('foo2/', views.main_template,name = 'new'),
    path('about/',views.about, name= 'about'),
    path('get_reply/',views.load_reply,name = 'ajax_perform_chat'),
    path('inital_message/',views.initial_load,name = 'initial_chat'),
    path('temp/',views.interviewer_page,name='temp'),
    path('temp2/',views.application_result,name='temp2'),
    path('redirect_interview/',views.redirect_interview,name = 'redirect_interview'),
    path('ajax_save/',views.set_accept,name='set_accept'),
    path('ajax_save2/',views.set_reject,name='set_reject')
]