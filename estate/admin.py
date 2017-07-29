from django.contrib import admin
from .models import *
from django import forms
from django.utils import timezone
from datetime import datetime



class BookingScheduleForm(forms.ModelForm):
    
    def clean(self):
        
        schedule_date = self.cleaned_data.get('schedule_date') 
        Bookingd = BookingDate.objects.filter(is_fully_booked = True) 
        dates = list(Bookingd)
        availabledates =[] 

        for date in dates: availabledates.append(date.scheduled_date)

        errormessage = []

        if schedule_date <= timezone.now():
            errormessage.append("S'il vous plaît sélectionnez une date valide.")     	
        
        if schedule_date not in availabledates :            
            errormessage.append("Cette date n'est pas disponible. Choisissez une autre date.")

        if errormessage:
            for i in errormessage:
              self.add_error('schedule_date', i)       
                
        return self.cleaned_data


class BookingDateForm(forms.ModelForm):
    
    def clean(self):
        
        scheduled_date = self.cleaned_data.get('scheduled_date')        

        if scheduled_date <= timezone.now():
            self.add_error('scheduled_date', "S'il vous plaît sélectionnez une date valide.")     	


class FormDownloadForm(forms.ModelForm):
    
    def clean(self):
        
        is_downloaded = self.cleaned_data.get('is_downloaded')
        is_validated = self.cleaned_data.get('is_validated')

        if not is_downloaded and is_validated: 
            self.add_error('is_validated', "Le client ne peut être validé que lorsque l'utilisateur a téléchargé les termes et conditions")          
	
class AnswerForm(forms.ModelForm):
    
    def clean(self):        
        
        quest = self.cleaned_data.get('question')

        if not quest.is_validated: 
            raise forms.ValidationError('La question doit être validée avant de répondre')                


class AddressInline(admin.StackedInline):
    model = Address
    verbose_name = "Adresse" 
    classes = ['collapse']

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    verbose_name = "Image de la propriété"
    classes = ['collapse']

class ThreeDViewInline(admin.TabularInline):
    model = ThreeDView 
    verbose_name = "Vu 3D" 
    classes = ['collapse']

class QuestionInline(admin.StackedInline):
    model = Question 
    classes = ['collapse']        

class AnswerInline(admin.StackedInline):
    model = Answer
    form = AnswerForm
    verbose_name = "Répondre"
    classes = ['collapse']  

class VoteInline(admin.TabularInline):
    model = Vote 
    classes = ['collapse']      

class FormDownloadInline(admin.TabularInline):    
    model = FormDownload
    form = FormDownloadForm
    verbose_name = "Conditions générales de téléchargement" 
    classes = ['collapse']

class PropertyDocumentInline(admin.TabularInline):
    model = PropertyDocument
    verbose_name = "Document de propriété" 
    classes = ['collapse']

class BookingScheduleInline(admin.StackedInline):
    model = BookingSchedule
    form = BookingScheduleForm
    verbose_name = "Horaire de réservation"
    classes = ['collapse'] 


class QuestionAdmin(admin.ModelAdmin):    
    inlines = [AnswerInline]
    list_display = ('place', 'user_profile', 'is_validated')
    search_fields = ['place__title']
    

class AnswerAdmin(admin.ModelAdmin):    
    inlines = [VoteInline]
    list_display = ('get_question_location', 'get_who_answered', 'date')
    search_fields = ['question__place__title']

    def get_question_location(self, obj):
        return obj.question.place.title
    get_question_location.short_description = 'Lieu Associé'
    
    def get_who_answered(self, obj):
        return obj.user_profile.user
    get_who_answered.short_description = 'Répondu par'   

class BookingScheduleAdmin(admin.ModelAdmin):    
    form = BookingScheduleForm
    list_display = ('schedule_date', 'place', 'first_name', 'last_name', 'email')
    list_filter = ('schedule_date','place' )
    search_fields = ['first_name', 'last_name','place']


class BookingDateAdmin(admin.ModelAdmin):
    form = BookingDateForm
    # actions = ['make_whole_day_available']

    # def make_whole_day_available(self, request, queryset):
    #     for object in queryset:
    #     	i=0
    #     	while i<24 :  
	   #      	new = BookingDate(scheduled_date = datetime.now())       
	   #      	new.scheduled_date.replace(hour=i)
	   #      	new.save()       	

    # make_whole_day_available.short_description = "Marquer toute la journée disponible"


        

    def expired(self, obj):
        return obj.scheduled_date >= timezone.now()
    expired.short_description = 'Date Valid?'
    expired.boolean = True

    def fullybooked(self, obj):
        return not obj.is_fully_booked
    fullybooked.short_description = 'Booking slot Available?'
    fullybooked.boolean = True

    list_display = ('scheduled_date', 'fullybooked', 'expired')


class PlaceAdmin(admin.ModelAdmin):

    inlines = [AddressInline, PropertyImageInline, ThreeDViewInline,  BookingScheduleInline, FormDownloadInline, PropertyDocumentInline,QuestionInline]

    date_hierarchy = 'created_date'
    filter_horizontal = ['facilities']
    list_display = ('title', 'get_location', 'property_type', 'age', 'area', 'price','floor', 'uploaded_by')   
    list_filter = ('address__location','floor' )
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'property_type__name', 'age', 'floor', 'facilities__name', 'address__location']

    def get_location(self, obj):
        return obj.address.location
    get_location.short_description = 'Location'
    get_location.admin_order_field = 'address__location'     



class ClientPropertyAdmin(admin.ModelAdmin):
    # inlines = [AddressInline, PropertyImageInline, ThreeDViewInline, QuestionInline, BookingScheduleInline, PropertyDocumentInline]
    list_display = ('property_type', 'area', 'city', 'selling_status', 'client_type', 'price')
    list_filter = ('property_type','client_type','selling_status')



class PropertyTypeAdmin(admin.ModelAdmin):
    pass

class FacilityAdmin(admin.ModelAdmin):
    pass

class OtherFieldAdmin(admin.ModelAdmin):
    pass    

admin.site.register(BookingSchedule, BookingScheduleAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(BookingDate, BookingDateAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(ClientProperty, ClientPropertyAdmin)
admin.site.register(OtherField, OtherFieldAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)




