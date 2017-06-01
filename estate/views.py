from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Place, PropertyType, Facility, OtherField, Place, UserProfile, BookingSchedule, BookingDate
from .serializers import PlaceSerializer
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.edit import ProcessFormView, FormMixin
from .forms import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from datetime import datetime


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


class SellView(TemplateView):
	template_name = 'estate/sell_page.html'

	def get_context_data(self, **kwargs):
		kwargs['form'] = ClientPropertyForm(prefix='client')
		kwargs['booking_form'] = PlaceInfoForm(prefix='book')
		return super(SellView, self).get_context_data(**kwargs)



class EstateView(TemplateView):
	template_name = "estate/estate.html"


class PropertyDetailView(DetailView, FormMixin, ProcessFormView):
	model = Place
	form_class = UserQuestionForm

	def get_form_kwargs(self):
		kwargs = super(PropertyDetailView, self).get_form_kwargs()
		if self.request.user.is_authenticated:
			user_profile = get_object_or_404(UserProfile, user=self.request.user)
			kwargs['initial'] = {'place': self.get_object(), 'user_profile': user_profile}
		return kwargs

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		kwargs['questions'] = self.object.questions.filter(is_validated=True)
		kwargs['booking_form'] = PlaceInfoForm(initial={'place': self.object})
		if self.request.user.is_authenticated:
			user = UserProfile.objects.get(user=self.request.user)
			try:
				kwargs['download_form'] = DownloadForm(initial={'user': user, 'property': self.object})
				kwargs['download_file'] = FormDownload.objects.get(user=user, is_downloaded=True, property=self.object, is_validated=True)
			except FormDownload.DoesNotExist:
				pass
			except UserProfile.DoesNotExist:
				pass
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
		return super(QuestionDetailView, self).get_context_data(**kwargs)


class AnswerFormView(LoginRequiredMixin, FormView):
	form_class = AnswerForm
	template_name = 'estate/answer_form.html'

	def get_success_url(self):
		pk = self.kwargs.get('pk')
		place = self.kwargs.get('place')
		return reverse("estate:question_detail", kwargs={'pk': pk, 'place': place})

	def form_valid(self, form):
		instance = form.save(commit=False)
		try:
			if self.request.user != instance.question.user_profile.user:
				instance.save()
		except UserProfile.DoesNotExist:
			pass
		return super(AnswerFormView, self).form_valid(form)

	def form_invalid(self, form):
		print(form.non_field_errors, form.errors.as_data())
		return super(AnswerFormView, self).form_invalid(form)


class PlaceInfoFormView(FormView):
	form_class = PlaceInfoForm
	template_name = 'estate/place_info_form.html'

	def form_valid(self,form):
		instance = form.save()
		return JsonResponse({'success':True, 'message': 'Successfully Booked'})
		# return HttpResponseRedirect(reverse("estate:property_detail", kwargs={'slug':instance.place.slug}))

	def form_invalid(self, form):
		print(form.errors.as_json())
		return JsonResponse({'success':False, 'message':'Not Successful', 'errors':form.errors.as_json()})
		# return super(PlaceInfoFormView, self).form_invalid(form)


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


class ClientPropertyFormView(TemplateView, ProcessFormView):
	template_name = "estate/download_page.html"

	def post(self, request, *args, **kwargs):
		context = {}
		client_form = ClientPropertyForm(request.POST, prefix='client')
		book_form = PlaceInfoForm(request.POST, prefix='book')
		print(client_form.data);
		if client_form.is_valid():
			client_instance = client_form.save(commit=False)
			if book_form.is_valid():
				book_instance = book_form.save()
				client_instance.booking = book_instance
				client_instance.save()
				context['status'] = 'Complete'
				context['message'] = 'form filled completely with no errors.'
				context['success'] = True
				return JsonResponse(context)
			context['status'] = 'Incomplete'
			context['message'] = 'client form filled completely, but errors on booking form'
			context['errors'] = book_form.errors.as_json()
			context['success'] = True
			return JsonResponse(context)
		else:
			print(client_form.data)
			context['status'] = 'Failed'
			context['success'] = False
			context['message'] = "Invalid form"
			context['errors'] = client_form.errors.as_json()
			return JsonResponse(context)


class WorkView(TemplateView):
	template_name = 'estate/work_page.html'


class DownloadView(LoginRequiredMixin, TemplateView):
	template_name = 'estate/download_page.html'

	def get_context_data(self, **kwargs):
		try:
			if self.request.user.is_authenticated:
				user = UserProfile.objects.get(user=self.request.user)
				kwargs['form_downloads'] = FormDownload.objects.filter(user=user, is_downloaded=False).select_related('property')
				kwargs['form'] = DownloadForm(initial={'user':user})
		except UserProfile.DoesNotExist:
			pass

		return super(DownloadView, self).get_context_data(**kwargs)


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


class ScheduledDatesAPIView(APIView):
	def get(self, request, format=None):
		schedules = BookingDate.objects.filter(is_fully_booked=False)
		data = {
			'schedules':schedules.values()
		}
		return Response(data)


class ProfileView(TemplateView):
	template_name = 'estate/profile.html'


class FormDownloadView(FormView):
	form_class = DownloadForm
	template_name = 'estate/download_form.html'

	def form_valid(self, form):
		instance = form.save(commit=False)

		try:
			form_download = FormDownload.objects.get(user=instance.user, property=instance.property)
			if not form_download.is_downloaded:
				form_download.is_downloaded = instance.is_downloaded
			form_download.is_validated = instance.is_validated
			form_download.save()
		except FormDownload.DoesNotExist:
			instance.save()
		return JsonResponse({'status': 'Success', 'message': "Form saved successfully", 'success': True})

	def form_invalid(self, form):
		return JsonResponse({'status': 'Failed', 'message': form.errors.as_json(), 'success': False})


def logout(request):
	auth_views.logout(request)
	return HttpResponseRedirect('/')
