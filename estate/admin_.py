from django.contrib import admin

from estate.models import *


# Register your models here.
# admin.site.register(Place)


class AddressInline(admin.StackedInline):
	model = Address


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
admin.site.register(BookingDate)
admin.site.register(BookingSchedule)
admin.site.register(ClientProperty)
admin.site.register(FormDownload)
admin.site.register(PropertyDocument)
