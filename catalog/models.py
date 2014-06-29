# -*- coding: utf-8 -*-

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.db.models import Q
from ckeditor.fields import RichTextField
import pytils
import datetime
from dashboard import string_with_title

class Category(MPTTModel):
    name = models.CharField(max_length=50, verbose_name=u'название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родительская категория')
    order = models.IntegerField(null=True, blank=True, verbose_name=u'порядок сортировки')
    slug = models.SlugField(max_length=128, verbose_name=u'url', unique=True, blank=True, help_text=u'заполнять не нужно')
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            if self.parent:
                self.slug = pytils.translit.slugify(self.name) + '_' + str(self.parent.id)
            else:
                self.slug = pytils.translit.slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        if not self.order:
            self.order = self.id
            self.save()
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Category.objects.get(slug=page_name)
        except:
            return None
    
    @staticmethod
    def get(id_):
        try:
            return Category.objects.get(id=int(id_))
        except:
            return None
    
    def breadcrumb(self):
        page = self
        breadcrumbs = []
        while page:
            breadcrumbs.append(page)
            page = page.parent
        breadcrumbs.reverse()
        return breadcrumbs[:-1]
        
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        app_label = string_with_title("catalog", u"Каталог")

    
    class MPTTMeta:
        order_insertion_by = ['name']
        
    def __unicode__(self):
        return '%s%s' % (' -- ' * self.level, self.name)
    
   

class Item(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'категория', related_name='items')
    name = models.CharField(max_length=512, blank=True, verbose_name=u'название')
    art = models.CharField(max_length=50, verbose_name=u'артикул')
    price = models.FloatField(verbose_name=u'цена')   
    desc = RichTextField(verbose_name=u'описание')
    desc_full = RichTextField(blank=True, default=u'', verbose_name=u'описание дополнительное', help_text= u'(рядом с ценой)')
    image = models.ImageField(upload_to=lambda instance, filename: 'uploads/items/' + pytils.translit.translify(filename),
                              max_length=510, blank=True, verbose_name=u'изображение')
    order = models.IntegerField(null=True, blank=True, verbose_name=u'порядок сортировки')
    slug = models.SlugField(max_length=250, verbose_name=u'url', unique=True, blank=True, help_text=u'заполнять не нужно')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'дата добавления')
    hidden = models.BooleanField(blank=True, default=False, verbose_name=u'товар скрыт из каталога')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = pytils.translit.slugify(self.name)[:100] + '_' + str(self.category.id)
        super(Item, self).save(*args, **kwargs)
        if not self.order:
            self.order = self.id
            self.save()
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Item.objects.get(slug=page_name)
        except:
            return None

    @staticmethod
    def search(query):
        return [p for p in Item.objects.filter(Q(name__icontains=query) |
                                               Q(art__icontains=query) |
                                               Q(desc__icontains=query) |
                                               Q(desc_full__icontains=query) )]
    
    @staticmethod
    def get(id_):
        try:
            return Item.objects.get(id=id_)
        except:
            return None
    
    
    def get_path(self):
        path = [self.category]
        while path[0].parent:
            path.insert(0, path[0].parent)
        return path
    
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'
        ordering=['order']
        app_label = string_with_title("catalog", u"Каталог")
        
    def __unicode__(self):
        return self.name
    
