from django import forms
from .models import Question, Answer, Vote


class ContactForm(forms.Form):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	email = forms.EmailField()
	phone_number = forms.CharField(max_length=12)
	subject = forms.CharField(max_length=150)
	message = forms.CharField(widget=forms.Textarea)


class PlaceInfoForm(forms.Form):
	place = forms.CharField(max_length=200, widget=forms.HiddenInput)
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	email = forms.EmailField()
	phone_number = forms.CharField(max_length=12)
	message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))


class UserQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		exclude = ['name', 'email']
		widgets = {
			'content': forms.Textarea(attrs={'rows': 3}),
			'place': forms.HiddenInput(),
			'user_profile': forms.HiddenInput()
		}


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		exclude = ['user_profile']
		widgets = {
			'content': forms.Textarea(attrs={'rows': 3}),
			'place': forms.HiddenInput()
		}


class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = '__all__'
		widgets = {
			'content': forms.Textarea(attrs={'rows': 3,'placeholder':"response to question..."}),
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