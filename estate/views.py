from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Place, PropertyType, Facility, OtherField, Place, UserProfile
from .serializers import PlaceSerializer
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.edit import ProcessFormView, FormMixin
from .forms import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator


# Create your views here.


class PlaceList(generics.ListAPIView):
	queryset = Place.objects.all()
	serializer_class = PlaceSerializer


class PlaceDetail(generics.RetrieveAPIView):
	lookup_field = 'slug'
	queryset = Place.objects.all()
	serializer_class = PlaceSerializer


class IndexView(TemplateView):
	template_name = "estate/index.html"


class AboutView(TemplateView):
	template_name = "estate/about_page.html"


class ContactView(FormView):
	template_name = "estate/contact_page.html"
	success_url = "/"
	form_class = ContactForm

	def form_valid(self, form):
		subject = form.cleaned_data['subject']
		message = form.cleaned_data['message']
		sender = form.cleaned_data['email']
		name = form.cleaned_data['name']
		recipients = ['info@example.com']
		send_mail(subject, message, sender, recipients)
		return HttpResponseRedirect('/thanks/')


class EstateView(TemplateView):
	template_name = "estate/estate.html"


class PropertyDetailView(DetailView, FormMixin, ProcessFormView):
	model = Place

	def get_form_kwargs(self):
		kwargs = super(PropertyDetailView, self).get_form_kwargs()
		if self.request.user.is_authenticated:
			user_profile = get_object_or_404(UserProfile, user=self.request.user)
			kwargs['initial'] = {'place': self.get_object(), 'user_profile': user_profile}
		return kwargs

	def get_form_class(self):
		if self.request.user.is_authenticated:
			return UserQuestionForm
		return QuestionForm

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		if self.request.user.is_authenticated:
			user_profile = get_object_or_404(UserProfile, user=self.request.user)
			kwargs['question_form'] = UserQuestionForm(initial={'place': self.object, 'user': user_profile})
		else:
			kwargs['question_form'] = QuestionForm()
		kwargs['contact_form'] = PlaceInfoForm(initial={'place':self.object.title})
		return super(PropertyDetailView, self).get_context_data(**kwargs)

	def get_success_url(self):
		slug = self.get_object().slug
		return reverse("estate:property_detail", kwargs={'slug': slug})

	def form_valid(self, form):
		form.save()
		return super(PropertyDetailView, self).form_valid(form)

	def form_invalid(self, form):
		self.object = self.get_object()
		print(form.non_field_errors, form.errors.as_data())
		return super(PropertyDetailView, self).form_invalid(form)


class QuestionDetailView(DetailView):
	model = Question

	def get_queryset(self):
		queryset = super(QuestionDetailView, self).get_queryset().select_related('place').prefetch_related(
			'answers__votes')
		return queryset

	def get_context_data(self, **kwargs):
		if self.request.user.is_authenticated:
			user_profile = get_object_or_404(UserProfile, user=self.request.user)
			kwargs['vote_form'] = VoteForm(initial={'user_profile': user_profile})
			kwargs['form'] = AnswerForm(initial={'question': self.get_object(), 'user_profile': user_profile})
		else:
			kwargs['form'] = AnswerForm(initial={'question': self.get_object()})
		return super(QuestionDetailView, self).get_context_data(**kwargs)


class AnswerFormView(LoginRequiredMixin, FormView):
	form_class = AnswerForm

	def get_success_url(self):
		pk = self.kwargs.get('pk')
		place = self.kwargs.get('place')
		return reverse("estate:question_detail", kwargs={'pk': pk, 'place': place})

	def form_valid(self, form):
		instance = form.save(commit=False)
		if self.request.user != instance.question.user_profile.user:
			instance.save()
		return super(AnswerFormView, self).form_valid(form)

	def form_invalid(self, form):
		print(form.non_field_errors, form.errors.as_data())
		return super(AnswerFormView, self).form_invalid(form)


class PlaceInfoFormView(FormView):
	form_class = PlaceInfoForm
	template_name = 'estate/place_info_form.html'


class VoteFormView(LoginRequiredMixin, FormView):
	form_class = VoteForm
	template_name = 'estate/question_detail.html'

	def form_valid(self, form):
		instance = form.save(commit=False)
		if self.request.user != instance.answer.user_profile.user:
			try:
				vote = Vote.objects.get(user_profile=instance.user_profile, answer=instance.answer)
				if vote.is_like != instance.is_like:
					vote.is_like = instance.is_like
					vote.save()
					status = "Updated"
				else:
					status = 'No Update'
			except Vote.DoesNotExist:
				instance.save()
				status = "Saved"
			likes = Vote.objects.filter(answer=instance.answer, is_like=True).count()
			dislikes = Vote.objects.filter(answer=instance.answer, is_like=False).count()
			return JsonResponse({'status': status, 'likes': likes, 'dislikes': dislikes})
		print('Failed')
		return JsonResponse({'status': "Failed"})




class PropertyOptions(APIView):
	def get(self, request, format=None):
		property_types = PropertyType.objects.distinct().values('id', 'name')
		facilities = Facility.objects.distinct().values('id', 'name')
		other_fields = OtherField.objects.distinct().values('id', 'field_name')
		options = {
			'propertyTypes': property_types,
			'facilities': facilities,
			'otherFields': other_fields
		}
		return Response(options)


class ProfileView(TemplateView):
	template_name = 'estate/profile.html'


def logout(request):
	auth_views.logout(request)
	return HttpResponseRedirect('/')
