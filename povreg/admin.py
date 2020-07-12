from django.contrib import admin
from .models import Car, Driver, Insurance, Officer
from django.forms import Textarea
from django.db import models


# Register your models here.
class CarInline(admin.TabularInline):
    model = Car
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 20})}
    }


class InsuranceInline(admin.TabularInline):
    model = Insurance
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 20})}
    }


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})}
    }
    list_display = (
        'v_plate',
        'v_make',
        'v_model',
        'v_country',
        'v_state',
        'is_commercial',
        'status',
        'registration',
        'driver',
        'owner',

        'insurance',
        'is_insured',
    )
    list_filter = ('v_country', 'v_state', 'v_make',)
    fieldsets = (
        (None, {
            'fields': ('v_plate', 'v_make', 'v_model')
        }),
        ('Registration Details', {
            'fields': ('v_country', 'v_state', 'is_commercial', 'status', 'registration')
        }),
        ('Driver & Insurance', {
            'fields': ('driver', 'owner', 'insurance',)
        }),
    )


def verify_item(modelAdmin, request, queryset):
    for item in queryset:
        item.verified = True
        item.save()


verify_item.short_description = "Verify Data"


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})}
    }
    list_display = (
        'last_name',
        'first_name',
        'dob',
        'phone_num',
        'country',
        'state',
        'license_num',
        'license_expiry',
        'is_expired',
        'verified',
    )
    list_filter = ('country', 'state', 'verified')
    fieldsets = (
        (None, {
            'fields': ('last_name', 'first_name', 'dob', 'phone_num')
        }),
        ('License', {
            'fields': ('country', 'state', 'license_num', 'license_expiry')
        }),
        ('Account', {
            'fields': ('user', 'verified',)
        })
    )
    inlines = [CarInline, InsuranceInline]
    actions = [verify_item, ]


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})}
    }
    list_display = (
        'driver',
        'company',
        'policy_num',
        'coverage_type',
        'expiry',
        'is_expired',
        'status',
        'car',
    )
    list_filter = ('company', 'status', 'coverage_type')
    fieldsets = (
        (None, {
            'fields': ('driver', 'company')
        }),
        ('Policy Overview', {
            'fields': ('policy_num', 'coverage_type', 'expiry', 'status')
        }),
    )
    inlines = [CarInline]


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})}
    }
    list_display = (
        'rank',
        'first_name',
        'last_name',
        'region',
        'unit',
        'badge_num',
        'id_num',
        'id_photo',
        'verified',
    )
    list_filter = ('region', 'unit', 'verified')
    fieldsets = (
        (None, {
            'fields': ('rank', 'last_name', 'first_name')
        }),
        ('Service', {
            'fields': ('region', 'unit')
        }),
        ('ID Details', {
            'fields': ('badge_num', 'id_num', 'id_photo')
        }),
        ('Account', {
            'fields': ('user', 'verified')
        })

    )
    actions = [verify_item, ]

