from django.contrib import admin

# Register your models here.

from .models import *

# admin.site.register(Task)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject1.js',)