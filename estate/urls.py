from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'estate'

api_patterns = [
	url(r'^places/$', views.PlaceList.as_view()),
	url(r'^places/options/$', views.PropertyOptions.as_view()),
	url(r'^places/(?P<slug>[\w-]+)/$', views.PlaceDetail.as_view()),
]
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name="index"),
	url(r'^about/$', views.AboutView.as_view(), name="about"),
	url(r'^contact/$', views.ContactView.as_view(), name="contact"),
	url(r'^api/', include(api_patterns)),
	url(r'^estate/property/answer/votes/', views.VoteFormView.as_view(), name="vote"),
	url(r'^estate/property/(?P<place>[\w-]+)/question/(?P<pk>[\w-]+)/answers/', views.AnswerFormView.as_view(),name="answer_form"),
	url(r'^estate/property/(?P<place>[\w-]+)/question/(?P<pk>[\w-]+)/', views.QuestionDetailView.as_view(), name="question_detail"),
	url(r'^estate/property/(?P<place>[\w-]+)/info/', views.PlaceInfoFormView.as_view(), name="place_info"),
	url(r'^estate/property/(?P<slug>[\w-]+)/', views.PropertyDetailView.as_view(), name="property_detail"),
	url(r'^estate/', views.EstateView.as_view(), name="estate")
]

urlpatterns = format_suffix_patterns(urlpatterns)
