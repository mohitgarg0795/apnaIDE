from django.contrib import admin

# Register your models here.

from .models import CodeHistory,Users

admin.site.register(CodeHistory)
admin.site.register(Users)