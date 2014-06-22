# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'order')
    ordering = ('order', )
    
admin.site.register(models.Slider, SliderAdmin)