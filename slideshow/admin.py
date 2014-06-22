# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class SliderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'order')
    ordering = ('order', )
    
admin.site.register(models.Slider, SliderAdmin)