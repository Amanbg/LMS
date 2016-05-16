from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.validators import validate_email
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.exceptions import ValidationError

from .forms import AddLeadForm, TeamAddLeadForm, PasswordResetForm, CommentForm
from users.models import MyUser
from leads.models import Lead
from comment.models import Comment
from category.models import Category
from leadsource.models import LeadSource
import json
import re


class LoginView(TemplateView):
    """
    Users log in to the system, if the username and password matches the django database then a httpresponse with true status
    pass to ajax in usersvalidate.js and return correspoding template
    """

    template_name = 'login.html'

    def post(self, request):
            username = request.POST.get('name', '')
            password = request.POST.get('pass', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponse(json.dumps({'status': 'True', 'msg': 'login Successfully..!', 'url': '/home/'}))
                else:
                    print "The password is valid but the account has been disabled"
            else:
                return HttpResponse(json.dumps({'status': 'False', 'msg': 'Please enter correct Username and Password'}))

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context


class HomeView(LoginRequiredMixin, TemplateView):

    """
    Home view for the users, after logged in. Unauthorized access leads to login page
    """

    login_url = '/'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context.update({'user': self.request.user})
            if self.request.user.is_staff:
                context['teamlead'] = True

            else:
                context['teamlead'] = False
                context['lead'] = Lead.objects.count()
                context['followuplead'] = Comment.objects.count()
        else:
            return HttpResponseRedirect(reverse('login-view'))
        return context


class AddLeadView(LoginRequiredMixin, FormView):

    """
    Add Lead in to the System
    """
    login_url = '/'
    template_name = 'caller/add_lead.html'
    form_class = AddLeadForm
    success_url = '/home/'

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            form = self.get_form()
            if form.is_valid():
                data_dict = dict(self.request.POST.items())
                data_dict['source'] = LeadSource.objects.get(id=data_dict['source'])
                del data_dict['csrfmiddlewaretoken']
                lead_obj = Lead(created_by=self.request.user, assign_to=self.request.user, **data_dict)
                lead_obj.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return HttpResponseRedirect(reverse('login-view'))

    def get_context_data(self, **kwargs):
        context = super(AddLeadView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super(AddLeadView, self).form_valid(form)


class LeadView(LoginRequiredMixin, TemplateView):

    """
    View the Lead List added so far
    """
    template_name = 'lead.html'
    login_url = '/'
    success_url = '/home/'
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            return render(request, 'lead.html')

    def get_context_data(self, **kwargs):
        context = super(LeadView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            leadobj = Lead.objects.all()
            paginator = Paginator(leadobj, self.paginate_by)
            page_no = self.request.GET.get('page', 1)

            try:
                leaddetail = paginator.page(page_no)
            except PageNotAnInteger:
                leaddetail = paginator.page(1)
            except EmptyPage:
                leaddetail = paginator.page(paginator.num_pages)

            context['leadobj'] = leaddetail
            context['lead'] = Lead.objects.count()
            context['page'] = paginator.page(page_no)
            context['paginator'] = paginator
            if self.request.user.is_staff:
                context['teamlead'] = True

            else:
                context['teamlead'] = False
        else:
            return HttpResponseRedirect(reverse('login-view'))
        return context


class GetLeadDetailMixin(object):

    """
    Mixin to get the lead object and check if form in valid or not
    """
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(reverse('login-view'))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        return obj

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return HttpResponseRedirect(reverse('login-view'))

    def get_context_data(self, **kwargs):
        context = super(GetLeadDetailMixin, self).get_context_data(**kwargs)
        return context


class GetLeadDetails(LoginRequiredMixin, GetLeadDetailMixin,  DetailView, FormView):

    """
    Mixin inherit in this function to get the details, detail view is used to get detail of a particular object
    """
    login_url = '/'
    success_url = reverse_lazy('home-view')
    template_name = 'get_leads_details.html'
    form_class = CommentForm
    model = Lead
    queryset = None
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        category1 = form.cleaned_data['category']
        sub_category1 = form.cleaned_data['sub_category']
        description1 = form.cleaned_data['description']
        package_offered1 = form.cleaned_data['package_offered']

        category2 = Category.objects.create(category_name=category1, sub_category=sub_category1, lead=Lead.objects.get(id=self.kwargs.get(self.pk_url_kwarg)))
        comm_desc = Comment.objects.create(description=description1, package_offered=package_offered1, created_by=self.request.user, lead=Lead.objects.get(id=self.kwargs.get(self.pk_url_kwarg)))
        # import ipdb; ipdb.set_trace()
        category2.save()
        comm_desc.save()

        return HttpResponseRedirect(reverse('home-view'))

    def get_context_data(self, **kwargs):
        context = super(GetLeadDetails, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                context['teamlead'] = True
            else:
                context['teamlead'] = False
            try:

                context['comment'] = Comment.objects.get(lead_id=self.kwargs.get(self.pk_url_kwarg)).description
                context['user1'] = Comment.objects.get(lead_id=self.kwargs.get(self.pk_url_kwarg)).created_by.first_name
            except:
                context['comment'] = None
            print "helllo :", context
        else:
            return HttpResponseRedirect(reverse('login-view'))
        return context


class CallerListView(LoginRequiredMixin, TemplateView):

    """
    Get Caller list
    """
    template_name = 'TeamLeader/caller_list.html'
    login_url = '/'
    success_url = '/home/'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(CallerListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            caller = MyUser.objects.filter(created_by=self.request.user)

            paginator = Paginator(caller, self.paginate_by)
            page_no = self.request.GET.get('page', 1)

            try:
                callerlist = paginator.page(page_no)
            except PageNotAnInteger:
                callerlist = paginator.page(1)
            except EmptyPage:
                callerlist = paginator.page(paginator.num_pages)

            context['caller'] = callerlist
            context['page'] = paginator.page(page_no)
            context['paginator'] = paginator

            return context
        return HttpResponseRedirect(reverse('login-view'))


class TeamAddLeadFormView(LoginRequiredMixin, FormView):

    """
    Team lead add lead form , here assign_to field is added to assign lead to the caller
    """
    template_name = "TeamLeader/addleadform.html"
    login_url = '/'
    form_class = TeamAddLeadForm
    success_url = '/home/'

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            form = self.get_form()
            if form.is_valid():
                data_dict = dict(self.request.POST.items())
                # print data_dict
                data_dict['source'] = LeadSource.objects.get(id=data_dict['source'])
                data_dict['assign_to'] = MyUser.objects.get(id=data_dict['assign_to'])

                del data_dict['csrfmiddlewaretoken']

                lead_obj = Lead(created_by=self.request.user,  **data_dict)
                lead_obj.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return HttpResponseRedirect(reverse('login-view'))

    def get_context_data(self, **kwargs):
        context = super(TeamAddLeadFormView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super(TeamAddLeadFormView, self).form_valid(form)


class UploadLeadView(TemplateView):

    """
    Upload lead to the system
    """
    template_name = 'TeamLeader/uploads_leads.html'

    def get_context_data(self, **kwargs):
        context = super(UploadLeadView, self).get_context_data(**kwargs)
        context.update({'data': LeadSource.objects.all()})
        return context


class FollowupView(TemplateView):
    """
    Follow up leads
    """
    template_name = "followuplead.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(FollowupView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            commobjct = Comment.objects.order_by('-created_on')
            paginator = Paginator(commobjct, self.paginate_by)
            page_no = self.request.GET.get('page', 1)

            try:
                leaddetail = paginator.page(page_no)
            except PageNotAnInteger:
                leaddetail = paginator.page(1)
            except EmptyPage:
                leaddetail = paginator.page(paginator.num_pages)

            context['commobjct'] = leaddetail
            context['followuplead'] = Comment.objects.count()
            context['page'] = paginator.page(page_no)
            context['paginator'] = paginator
            if self.request.user.is_staff:
                context['teamlead'] = True

            else:
                context['teamlead'] = False
        else:
            return HttpResponseRedirect(reverse('login-view'))
        return context


class ResetPasswordView(LoginRequiredMixin, FormView):

    """
    Reset password by the Users
    """
    login_url = '/'
    template_name = 'reset_password.html'
    form_class = PasswordResetForm
    success_url = '/home/'

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                context['teamlead'] = True
            else:
                context['teamlead'] = False
        else:
            return HttpResponseRedirect(reverse('login-view'))
        return context

    def form_valid(self, form):
        return super(ResetPasswordView, self).form_valid(form)


class LogoutView(TemplateView):

    """
    Logout by the Users
    """
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def SearchView(request):
    """
    Search lead by email_id or contact no.
    """
    if request.method == "GET":

        q1 = request.GET.get('search_box', '')
        m1 = re.search('([7|8|9]\d{9})', q1)
        if m1 and m1.group():
            qs = Lead.objects.get(contact=q1)
            return render(request, 'lead.html', {'searchdata': qs})
        else:
            try:
                validate_email(q1)
                qs = Lead.objects.get(email_id=q1)
                return render(request, 'lead.html', {'searchdata': qs})
            except ValidationError as e:
                print "Please fill correct email_id"

        return HttpResponseRedirect('/home/')
