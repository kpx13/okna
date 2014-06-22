# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'parent', 'slug', 'order', 'id')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'art', 'price', 'hidden')
    search_fields = ['name', ]
    list_filter = ('category', 'hidden')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Item, ItemAdmin)