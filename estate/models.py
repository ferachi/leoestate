from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.validators import ValidationError
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from .utils import *
from django.urls import reverse


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
		('o', 'Ancien'),
		('n', 'Moderne')
	)
	PURCHASE = (
		('b', 'BUY'),
		('r', 'RENT')
	)
	title = models.CharField("Titre", max_length=255, unique=True)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	description = models.TextField("Description")
	property_type = models.ForeignKey('PropertyType', verbose_name="Type de propriété", on_delete=models.CASCADE,
	                                  related_name='places')
	price = models.DecimalField("Prix", max_digits=20, decimal_places=2)
	age = models.CharField("Âge", max_length=1, choices=AGE, default='o')
	no_rooms = models.PositiveIntegerField("Nombre de pièces", null=True, blank=True)
	no_bedrooms = models.PositiveIntegerField("Nombre de chambres", null=True, blank=True)
	area = models.PositiveIntegerField("Surface", null=True, blank=True)
	floor = models.CharField("Les étage", max_length=20, blank=True)
	monthly_charges = models.DecimalField("Frais mensuels", max_digits=10, decimal_places=2, blank=True, null=True)
	property_tax = models.DecimalField("Taxe de propriété", max_digits=10, decimal_places=2, blank=True, null=True)
	facilities = models.ManyToManyField('Facility', verbose_name="Facility (Critères avancés)", related_name='places',
	                                    blank=True)
	other_fields = models.ManyToManyField('OtherField', verbose_name='Caractéristique supplémentaire',
	                                      related_name='places', blank=True)
	thumbnail = models.ImageField("Image thumbnail", upload_to=upload_display_image_dir, null=True, blank=True,
	                              help_text='image thumbnail')
	image = models.ImageField("Afficher l'image", upload_to=upload_thumbnail_dir, null=True, blank=True,
	                          help_text="display image")
	uploaded_by = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="Telechargé par",
	                                related_name='place_uploads')
	created_date = models.DateTimeField(auto_now_add=True)
	timestamp = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		reverse('estate:property_detail', kwargs={"slug": "self.slug"})

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Place, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Propriétés (Acheter)"
		verbose_name_plural = "Propriétés (Acheter)"


class Address(models.Model):
	house_no = models.PositiveIntegerField("Numéro de maison / Appartement", null=True, blank=True)
	street = models.CharField("Rue", max_length=255, blank=True, null=True)
	city = models.CharField("Ville", max_length=120)
	town = models.CharField("Commune", max_length=120, blank=True, null=True)
	zip_code = models.PositiveIntegerField("Code Postal")
	location = models.CharField(max_length=255)
	latitude = models.DecimalField("Latitude", max_digits=16, decimal_places=8)
	longitude = models.DecimalField("Longitude", max_digits=16, decimal_places=8)
	place = models.OneToOneField(Place, verbose_name="Lieu", on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % self.place

	class Meta:
		verbose_name = 'Adress'
		verbose_name_plural = 'Adresses'


class PropertyImage(models.Model):
	title = models.CharField("Titre", max_length=20)
	description = models.CharField("Description", max_length=40)
	image = models.ImageField(upload_to=upload_place_images_dir, null=True, blank=True)
	place = models.ForeignKey(Place, verbose_name="Lieu", on_delete=models.CASCADE, related_name='images')

	def __str__(self):
		return self.title


class ThreeDView(models.Model):
	title = models.CharField("Titre", max_length=20)
	place = models.ForeignKey(Place, verbose_name="Le Lieu", on_delete=models.CASCADE, related_name='three_d_views')

	def __str__(self):
		return self.title


class PropertyType(models.Model):
	name = models.CharField("Nom", max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Type de propriété"
		verbose_name_plural = "Type de propriété"


class Facility(models.Model):
	name = models.CharField("Nom", max_length=120)
	quantity = models.CharField("Quantité", max_length=6)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Facility(Critères avancés)"
		verbose_name_plural = "Facility(Critères avancés)"
		unique_together = ('name', 'quantity')


class OtherField(models.Model):
	TYPE = (
		('t', 'Texte'),
		('n', 'Nombre'),
		('c', 'Devise')
	)
	field_name = models.CharField("Nom", max_length=20)
	field_type = models.CharField("Type", max_length=1, choices=TYPE, default='t')
	field_value = models.CharField("valeur", max_length=255)

	def __str__(self):
		return " ".join([self.field_name, self.field_value])

	class Meta:
		unique_together = ['field_name', 'field_type', 'field_value']
		verbose_name = "Caractéristique supplémentaires"
		verbose_name_plural = "Caractéristiques supplémentaires"


class BuyablePlace(Place):
	is_sold = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Place'
		verbose_name_plural = 'Places'


class Question(models.Model):
	place = models.ForeignKey(Place, verbose_name="Lieu", on_delete=models.CASCADE, related_name='questions')
	user_profile = models.ForeignKey(UserProfile, verbose_name="profil de l'utilisateur", on_delete=models.DO_NOTHING,
	                                 related_name='questions', null=True)
	name = models.CharField("Nom", max_length=100, blank=True)
	email = models.EmailField(null=True, blank=True)
	content = models.TextField("Question")
	date = models.DateTimeField(auto_now_add=True)
	is_validated = models.BooleanField("Valide?", default=False)

	#  def __str__(self):
	#     if self.place:
	#         return "By %s" % self.user_profile
	def __str__(self):
		if self.place:
			return "By %s:  %s" % (self.user_profile, self.content)

	class Meta:
		ordering = ['-date']


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
	user_profile = models.ForeignKey(UserProfile, verbose_name="profil de l'utilisateur", on_delete=models.DO_NOTHING,
	                                 related_name='answers')
	content = models.TextField("Répondre")
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.question:
			return "By %s" % self.user_profile

	class Meta:
		ordering = ['-date']
		unique_together = ('user_profile', 'question')
		verbose_name = "Réponses à la question"


class Vote(models.Model):
	answer = models.ForeignKey(Answer, verbose_name="Répondre", on_delete=models.CASCADE, related_name='votes')
	user_profile = models.ForeignKey(UserProfile, verbose_name="profil de l'utilisateur", on_delete=models.DO_NOTHING,
	                                 related_name='votes')
	is_like = models.NullBooleanField("accepté?", null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.answer:
			return "%s By %s" % ("Votez pour la réponse associée", self.user_profile)

	class Meta:
		ordering = ['-date']
		verbose_name = "Votez pour la réponse"


class BookingSchedule(models.Model):
	place = models.ForeignKey(Place, verbose_name="Lieu", on_delete=models.CASCADE, related_name='booking_schedules',
	                          null=True, blank=True)
	first_name = models.CharField("Prénom", max_length=30, error_messages={'required': 'ce champ est requis'})
	last_name = models.CharField("nom", max_length=30, error_messages={'required': 'ce champ est requis'})
	email = models.EmailField("Votre email", max_length=50, error_messages={'required': 'ce champ est requis'})
	phone_number = models.CharField("Votre numéro de téléphone", max_length=15)
	message = models.TextField("votre message", error_messages={'required': 'ce champ est requis'})
	schedule_date = models.DateTimeField("Date du calendrier", error_messages={'required': 'ce champ est requis'})
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		date_time = self.schedule_date.strftime("%H:%M, %d/%m/%Y")
		if self.place:
			return "%s à voir %s on %s" % (self.first_name, self.place.title, date_time)
		return "%s  %s" % (self.first_name, self.schedule_date)

	class Meta:
		verbose_name = "Date prévue"
		verbose_name_plural = "Dates prévue"


class BookingDate(models.Model):
	scheduled_date = models.DateTimeField("Date disponible", unique=True)
	is_fully_booked = models.BooleanField("Réservation complète?", default=False)

	def __str__(self):
		return "%s" % self.scheduled_date.strftime("time - %H:%M , date - %d/%m/%Y")

	def is_expired(self):
		return self.date < datetime.now().date()

	is_expired.short_description = "is_expired"

	class Meta:
		verbose_name = "Dates disponible"
		ordering = ['scheduled_date']


class FormDownload(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name="profil de l'utilisateur")
	property = models.ForeignKey(Place)
	is_downloaded = models.BooleanField("Téléchargé?", default=False)
	is_validated = models.BooleanField("Validé?", default=False)

	# define a toString method here
	def __str__(self):
		return "%s - %s" % (self.property, "Termes et Conditions Acceptation et Validation")


class PropertyDocument(models.Model):
	place = models.ForeignKey('Place', verbose_name="Lieu", on_delete=models.CASCADE, related_name='documents')
	upload_by = models.ForeignKey('UserProfile', verbose_name="profil de l'utilisateur")
	document_name = models.CharField("Nom du document", max_length=50)
	is_downloaded = models.BooleanField("Téléchargé?", default=False)
	upload = models.FileField()
	upload_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.document_name


class ClientProperty(models.Model):
	PROPERTY_TYPE = (
		('MV', 'Maison/Villa'),
		('AP', 'Apartement')
	)
	NO_ROOMS = (
		('a', '1'),
		('b', '2'),
		('c', '3'),
		('d', '4'),
		('e', '5'),
		('f', '6 et +'),
	)
	SELLING_STATUS = (
		('a', 'Oui, j’ai déjà commencé la vente'),
		('b', 'Oui, dès que possible'),
		('c', 'Oui, d’ici 3 mois'),
		('d', 'Oui, d’ici 6 mois'),
		('e', 'Oui, dans plus de 6 mois'),
		('f', 'Non, je n’ai pas de projet de vente'),
	)
	CLIENT_TYPE = (
		('VE', 'Vendre'),
		('ES', 'Estimer')
	)
	property_type = models.CharField("Type de bien", max_length=2, choices=PROPERTY_TYPE, default='MV')
	no_rooms = models.CharField("Nombre de pièce(s)", max_length=1, choices=NO_ROOMS, default='a')
	land_area = models.PositiveIntegerField("Surface terrain")
	no_bathrooms = models.CharField("Nombre de salle de bains", max_length=1, choices=NO_ROOMS, default='a')
	area = models.PositiveIntegerField("Surface")
	price = models.PositiveIntegerField("Prix demandé")
	address = models.CharField("Nom de la rue", max_length=400)
	postal_code = models.PositiveIntegerField("Code postal")
	city = models.CharField("Ville", max_length=100)
	year_constructed = models.PositiveIntegerField("Année de construction")
	selling_status = models.CharField("Envisagez-vous de vendre ce bien ?", max_length=1, choices=SELLING_STATUS,
	                                  default='a')
	facilities = models.CharField(max_length=300, blank=True)
	booking = models.ForeignKey('BookingSchedule', related_name='client_properties', null=True, blank=True,
	                            on_delete=models.DO_NOTHING)
	client_type = models.CharField(max_length=2, choices=CLIENT_TYPE, default='VE', blank=True)

	class Meta:
		verbose_name = "Propriétés (Vendre)"
		verbose_name_plural = "Propriétés (Vendre)"



