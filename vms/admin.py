from django.contrib import admin

from . models import Visitor, Visitee, Visit, Gate



# Register your models here.
admin.site.register(Visitor)
admin.site.register(Visitee)
admin.site.register(Visit)
admin.site.register(Gate)