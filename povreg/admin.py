from django.contrib import admin
from .models import Car, Driver, Insurance, Officer

# Register your models here.
admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(Insurance)
admin.site.register(Officer)

