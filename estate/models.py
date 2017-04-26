from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .utils import *


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.userprofile.save()


class Place(models.Model):
	AGE = (
		('o', 'OLD'),
		('n', 'NEW')
	)
	PURCHASE = (
		('b', 'BUY'),
		('r', 'RENT')
	)
	title = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	description = models.TextField()
	property_type = models.ForeignKey('PropertyType', on_delete=models.CASCADE, related_name='places')
	price = models.DecimalField(max_digits=20, decimal_places=2)
	age = models.CharField(max_length=1, choices=AGE, default='o')
	no_rooms = models.PositiveIntegerField("Number of Rooms", null=True, blank=True)
	no_bedrooms = models.PositiveIntegerField("Number of Bedrooms", null=True, blank=True)
	area = models.PositiveIntegerField(null=True, blank=True)
	floor = models.CharField(max_length=20, blank=True)
	monthly_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	property_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	facilities = models.ManyToManyField('Facility', related_name='places', blank=True)
	other_fields = models.ManyToManyField('OtherField', related_name='places', blank=True)
	thumbnail = models.ImageField("Image thumbnail", upload_to=upload_display_image_dir, null=True, blank=True,
	                              help_text='image thumbnail')
	image = models.ImageField("Display Image", upload_to=upload_thumbnail_dir, null=True, blank=True,
	                          help_text="display image")
	uploaded_by = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='place_uploads')
	created_date = models.DateTimeField(auto_now_add=True)
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Place, self).save(*args, **kwargs)


class Address(models.Model):
	house_no = models.PositiveIntegerField(null=True, blank=True)
	street = models.CharField(max_length=255, blank=True, null=True)
	city = models.CharField(max_length=120)
	town = models.CharField(max_length=120, blank=True, null=True)
	location = models.CharField(max_length=255)
	postal_code = models.CharField(max_length=10)
	latitude = models.DecimalField(max_digits=16, decimal_places=8)
	longitude = models.DecimalField(max_digits=16, decimal_places=8)
	place = models.OneToOneField(Place, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Addresses'


class PropertyImage(models.Model):
	title = models.CharField(max_length=20)
	description = models.CharField(max_length=40)
	image = models.ImageField(upload_to=upload_place_images_dir, null=True, blank=True)
	place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')

	def __str__(self):
		return self.title


class ThreeDView(models.Model):
	title = models.CharField(max_length=20)
	place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='three_d_views')

	def __str__(self):
		return self.title


class PropertyType(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Facility(models.Model):
	name = models.CharField(max_length=120)
	quantity = models.PositiveIntegerField()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "facilities"
		unique_together = ('name', 'quantity')


class OtherField(models.Model):
	TYPE = (
		('t', 'Text'),
		('n', 'Number'),
		('c', 'Currency')
	)
	field_name = models.CharField(max_length=20)
	field_type = models.CharField(max_length=1, choices=TYPE, default='t')
	field_value = models.CharField(max_length=255)

	def __str__(self):
		return " ".join([self.field_name, self.field_value])

	class Meta:
		unique_together = ['field_name', 'field_type', 'field_value']


class RentablePlace(Place):
	TYPES = (
		('m', 'Month'),
		('y', 'Year'),
		('w', 'Week'),
		('d', 'Day')
	)
	duration = models.PositiveIntegerField()
	is_rented = models.BooleanField(default=False)
	duration_type = models.CharField(max_length=1, choices=TYPES, default='m')
	total_duration_months = models.PositiveIntegerField(null=True, blank=True)


class BuyablePlace(Place):
	is_sold = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Place'
		verbose_name_plural = 'Places'


class Question(models.Model):
	place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='questions')
	user_profile = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='questions', null=True)
	name = models.CharField(max_length=100, blank=True)
	email = models.EmailField(null=True, blank=True)
	content = models.TextField("Question")
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date']


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
	user_profile = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='answers')
	content = models.TextField("Answer")
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date']
		unique_together = ('user_profile', 'question')


class Vote(models.Model):
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
	user_profile = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name='votes')
	is_like = models.NullBooleanField(null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date']
