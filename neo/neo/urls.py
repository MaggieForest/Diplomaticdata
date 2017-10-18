# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import view,search,search2,addc
 
urlpatterns = [
    url(r'^hello$', view.hello),
    url(r'^search-form$', search.search_form),
    url(r'^search$', search.search),
    url(r'^search-post$', search2.search_post),
    url(r'^addindex$', addc.index),
    url(r'^add$', addc.add),
    url(r'^near',view.near),
    url(r'^find_near',view.find_near),
    url(r'^path',view.path),
    url(r'^find_path',view.find_path),
]