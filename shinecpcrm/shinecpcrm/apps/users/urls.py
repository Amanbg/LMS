from django.conf.urls import url
from .views import LoginView, HomeView, LeadView,  AddLeadView, TeamAddLeadFormView,  UploadLeadView, GetLeadDetails, FollowupView, ResetPasswordView, LogoutView, CallerListView
from . import views

urlpatterns = [

    url(r'^$', view=LoginView.as_view(), name='login-view'),
    url(r'^home/', view=HomeView.as_view(), name='home-view'),
    url(r'^lead/$', view=LeadView.as_view(), name='LeadViews'),
    url(r'addlead/$', view=AddLeadView.as_view(), name='AddLeadView'),
    url(r'teamleadform/$', view=TeamAddLeadFormView.as_view(), name='Team-Lead-View'),
    url(r'getleaddetails/(?:id=(?P<id>\d+)/)?$', view=GetLeadDetails.as_view(), name='Get-Lead-Details'),
    url(r'uploadleads/$', view=UploadLeadView.as_view(), name='Upload-Lead'),
    url(r'get-caller-list/$', view=CallerListView.as_view(), name='Caller-List-View'),
    url(r'follow-up-lead/$', view=FollowupView.as_view(), name='followuplead'),
    url(r'reset_password/$', view=ResetPasswordView.as_view(), name='Reset_Password_View'),
    url(r'^logout/$', view=LogoutView.as_view(), name='LogoutView'),
    url(r'^search/$', views.SearchView, name='searchbarview'),

]
