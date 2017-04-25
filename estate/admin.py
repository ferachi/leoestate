from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Place)


class AddressInline(admin.StackedInline):
	model = Address


@admin.register(RentablePlace)
class RentablePlaceAdmin(admin.ModelAdmin):
	inlines = [
		AddressInline
	]


@admin.register(BuyablePlace)
class BuyablePlaceAdmin(admin.ModelAdmin):
	inlines = [
		AddressInline
	]


admin.site.register(PropertyType)
admin.site.register(Facility)
admin.site.register(PropertyImage)
admin.site.register(OtherField)
admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)