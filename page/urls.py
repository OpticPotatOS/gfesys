# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.conf.urls import patterns, url

# This file handles what url's are mapped to what view.
# This is much better explained in the Django manual,
# and we don't do anything freakier than what is explained in the tutorials. Promise <3
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

from page import views

urlpatterns = patterns('',
	url(r'^(?P<page_id>\d+)/$', views.page, name='page'),
	url(r'^edit/(?P<page_id>\d+)/$', views.edit_page, name='edit_page'),
	url(r'^new/$', views.new_page, name='new_page'),
)