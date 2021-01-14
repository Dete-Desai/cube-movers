from django.contrib import admin
from .models import (
    Source, Vehicle, MoveType, Room, QuoteItemType, QuoteItemDefault,
    Settings, StaffProfile, Item, Branch, Office, Customer
)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'registration', 'cbm')
    list_filter = ('make', 'model', 'registration', 'cbm')
    search_fields = ['make', 'model', 'registration', 'cbm']


class MoveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency')
    list_filter = ('name', 'currency')
    search_fields = ['name', 'currency']


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


class QuoteItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


class QuoteItemDefaultAdmin(admin.ModelAdmin):
    list_display = ('item', 'cost', 'quote_item_type')
    search_fields = ['item', 'cost']
    list_filter = ('quote_item_type',)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ['name']


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'code')
    search_fields = ['user__first_name', 'user__username', 'code']


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'vol')
    search_fields = ['name']

admin.site.register(Source, SourceAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(MoveType, MoveTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(QuoteItemType, QuoteItemTypeAdmin)
admin.site.register(QuoteItemDefault, QuoteItemDefaultAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Branch)
admin.site.register(Office)
admin.site.register(Customer)
