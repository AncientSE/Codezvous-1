# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:54:46 2017

@author: ricky
"""

from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register$', views.UserFormView.as_view(), name = 'register'),
    url(r'^$', views.homepage, name='homepage'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^login$', auth_views.login, {'template_name': 'ancient/login.html'}, name='login'),
    url(r'^submit/1/$', views.submit_new, name='submit_1'),

    #student
    url(r'^student/home/cs/(?P<classnumber>\d+)/$', views.student_home_cs, name='student_home_cs'), # student homepage for class content
    url(r'^student/course/main/(?P<classnumber>\d+)/$', views.student_course_main, name='student_course_main'),
    url(r'^student/course/(?P<classnumber>\d+)/(?P<homeworknumber>\d+)/$', views.student_course_hw, name='student_course_hw'),

    #teacher
    url(r'^teacher/home/ct/(?P<classnumber>\d+)/$', views.teacher_home_ct, name='teacher_home_ct'),
    url(r'^teacher/course/main/(?P<classnumber>\d+)/$', views.teacher_course_main, name='teacher_course_main'),
    url(r'^teacher/course/(?P<classnumber>\d+)/(?P<homeworknumber>\d+)/$', views.teacher_course_hw, name='teacher_course_hw')
]