# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
 
from pages.models import Page
from slideshow.models import Slider
from news.models import NewsItem
from catalog.models import Category, Item

import config
from livesettings import config_value
from django.conf import settings

NEWS_PAGINATION_COUNT = 10
PAGINATION_COUNT = 16

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

def gallery(request):
    c = get_common_context(request)
    c['title'] = u'Галерея'
    return render_to_response('gallery.html', c, context_instance=RequestContext(request))

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

def filter_items(request, c, items):
    paginator = Paginator(items, PAGINATION_COUNT)
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
    c['items'] = items
    return c

def category(request, slug):
    c = get_common_context(request)
    if slug:
        c['category'] = Category.get_by_slug(slug)
        c['title'] = c['category'].name
        items = Item.objects.filter(category__in=c['category'].get_descendants(include_self=True), hidden=False)
        if c['category'].parent:
            c['subcategories'] = c['category'].parent.get_descendants().extra(order_by = ['id'])
        else:
            c['subcategories'] = c['category'].get_descendants().extra(order_by = ['id'])
    else:
        items = Item.objects.all()
        c['subcategories'] = Category.objects.filter(parent=None)
        c['title'] = u'Каталог'
    return render_to_response('category.html', filter_items(request, c, items), context_instance=RequestContext(request))

def item(request, slug):
    c = get_common_context(request)
    c['item'] = Item.get_by_slug(slug)
    c['category'] = c['item'].category
    c['title'] = c['item'].name
    return render_to_response('item.html', c, context_instance=RequestContext(request))