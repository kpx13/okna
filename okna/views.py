# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
 
from pages.models import Page
from slideshow.models import Slider
from news.models import NewsItem

import config
from livesettings import config_value
from django.conf import settings

NEWS_PAGINATION_COUNT = 10

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['news_recent'] = NewsItem.objects.all()[0:4]
    c.update(csrf(request))
    return c

def page(request, page_name):
    c = get_common_context(request)
    p = Page.get_by_slug(page_name)
    if p:
        c.update({'p': p})
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    else:
        raise Http404()

def home(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['slider'] = Slider.objects.all()
    c['p'] = Page.get_by_slug('home')
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def news(request, slug=None):
    c = get_common_context(request)
    if slug == None:
        items = NewsItem.objects.all()
        paginator = Paginator(items, NEWS_PAGINATION_COUNT)
        page = int(request.GET.get('page', '1'))
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            items = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            items = paginator.page(page)
        c['page'] = page
        c['page_range'] = paginator.page_range
        if len(c['page_range']) > 1:
            c['need_pagination'] = True
        
        c['news'] = items
        return render_to_response('news.html', c, context_instance=RequestContext(request))
    else:
        c['new'] = NewsItem.get_by_slug(slug)
        return render_to_response('new.html', c, context_instance=RequestContext(request))