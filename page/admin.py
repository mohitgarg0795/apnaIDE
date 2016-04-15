from django.contrib import admin

# Register your models here.

from .models import CodeHistory,Textpaduser

admin.site.register(CodeHistory)
admin.site.register(Textpaduser)