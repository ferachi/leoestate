from django import forms
from .models import Question, Answer, Vote, BookingSchedule, FormDownload, ClientProperty
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
	first_name = forms.CharField(max_length=50, label="Prénom")
	last_name = forms.CharField(max_length=50, label="Nom")
	email = forms.EmailField(label="Votre email")
	phone_number = forms.CharField(label="Votre numéro de téléphone", max_length=12)
	subject = forms.CharField(max_length=150)
	message = forms.CharField(label="Votre message", widget=forms.Textarea(attrs={'rows': 3}))


class PlaceInfoForm(forms.ModelForm):
	class Meta:
		model = BookingSchedule
		fields = '__all__'
		widgets = {
			'message': forms.Textarea(attrs={'rows':4}),
			'place':forms.HiddenInput()
		}
		error_messages = {
			'first_name': {
				'required': _("ce champ est requis"),
			},
			'last_name': {
				'required': _("ce champ est requis"),
			},
			'schedule_date': {
				'required': _("ce champ est requis"),
				'invalid': _("entrez une date valide")
			},
			'phone_number': {
				'required': _("ce champ est requis"),
			},
			'email': {
				'required': _("ce champ est requis"),
				'invalid': _("entrez une adresse mail valide")
			},
			'message': {
				'required': _("ce champ est requis"),
			},
		}


class UserQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		exclude = ['name', 'email', 'is_validated']
		widgets = {
			'content': forms.Textarea(attrs={'rows': 3}),
			'place': forms.HiddenInput(),
			'user_profile': forms.HiddenInput()
		}


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		exclude = ['user_profile', 'is_validated']
		widgets = {
			'content': forms.Textarea(attrs={'rows': 3}),
			'place': forms.HiddenInput()
		}


class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = '__all__'
		widgets = {
			'content': forms.Textarea(attrs={'rows': 3,'placeholder':"Répondre à la question..."}),
			'question': forms.HiddenInput(),
			'user_profile': forms.HiddenInput()
		}


class VoteForm(forms.ModelForm):
	class Meta:
		model = Vote
		fields = '__all__'
		widgets = {
			'is_like': forms.HiddenInput(),
			'answer': forms.HiddenInput(),
			'user_profile': forms.HiddenInput()
		}


class DownloadForm(forms.ModelForm):
	class Meta:
		model = FormDownload
		exclude = ['is_validated', 'document']

		widgets = {
			'property':forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'is_downloaded' : forms.HiddenInput()
		}


class ClientPropertyForm(forms.ModelForm):
	class Meta:
		model = ClientProperty
		fields = '__all__'

		widgets = {
			'year_constructed': forms.TextInput(),
			'land_area': forms.TextInput(),
			'area': forms.TextInput(),
			'price': forms.TextInput(),
			'postal_code': forms.TextInput(),
		}

		error_messages = {
			'address': {
				'required': _("ce champ est requis"),
			},
			'postal_code': {
				'invalid': _("Cette valeur doit être un nombre"),
				'required': _("ce champ est requis")
			},
			'area': {
				'invalid': _("Cette valeur doit être un nombre"),
				'required': _("ce champ est requis")
			},
			'land_area': {
				'invalid': _("Cette valeur doit être un nombre"),
				'required': _("ce champ est requis"),
			},
			'city': {
				'required': _("ce champ est requis")
			},
			'year_constructed': {
				'invalid': _("Cette valeur doit être un nombre"),
				'required': _("ce champ est requis"),
			},
			'price': {
				'invalid': _("Cette valeur doit être un nombre"),
				'required': _("ce champ est requis")
			}
		}


