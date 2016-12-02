from django.views.generic import ListView, DetailView, View, TemplateView

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from django.utils.timezone import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import Http404

from django.contrib.auth.decorators import login_required
from base.views import GenericSelfRedirection, GenericModalUpdateView


from .models import Contact, Communication
from .forms import ContactForm, CommunicationForm, ContactUpdateForm, DeleteCommForm


class DashBoardView(PermissionRequiredMixin, ListView):
    template_name = 'dashboard.html'
    model = Communication

    permission_required = 'auth.add_user'

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        context['followup_count'] = Communication.objects.filter(
            next_followup__date=datetime.today()).count()
        context['hot_count'] = Contact.objects.filter(status=3).count()
        context['proposed_count'] = Contact.objects.filter(status=5).count()
        context['proposal_count'] = Contact.objects.filter(status=9).count()
        return context


class ContactView(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['form'] = ContactForm()
        # context['contact'] = Contact.objects.get(pk=self.kwargs.get('pk'))
        # context['hot_count'] = Contact.objects.filter(status='Hot').count()
        context['user'] = self.request.user
        try:
            groups = self.request.user.groups.all()
            groups = [group.name for group in groups]
        except:
            raise Http404(
                "User is not assigned to any group,Please assign and Try again")
        if 'sales' in groups:
            groups.remove('sales')
            context['contacts'] = [
                contact for contact in Contact.objects.filter(
                    group__name=groups[0])
            ]
        else:
            context['contacts'] = Contact.objects.all()
        return context


class ModalCreateView(
    PermissionRequiredMixin,
    GenericSelfRedirection
):
    form_class = ContactForm
    object_name = 'Contact'
    permission_required = 'crm.add_crm'
    url_pattern_list = ['crm', 'detail']
    error_url = '/crm/list/'


class CrmDetailView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(CrmDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['contact'] = Contact.objects.get(pk=self.kwargs.get('pk'))
        context['follow'] = Communication.objects.filter(
            next_followup__gte=datetime.now())
        context['form'] = CommunicationForm()
        context['form1'] = ContactUpdateForm(instance=context['contact'])

        # context['del'] = Communication.objects.last().delete()
        print "+++++++++"
        print context['follow']
        print "+++++++++"
        return context


class CrmupdateView(
    PermissionRequiredMixin, GenericModalUpdateView
):

    permission_required = 'customer.add_customer'
    form_class = ContactUpdateForm
    object_name = 'Contact'
    model = Contact
    app_url = '/crm/'
    page_url = '/detail/'

    def get_success_url(self):
        return '/crm/detail/{0}'.format(self.kwargs.get('pk'))


class CrmFollowUpView(LoginRequiredMixin, ListView):
    template_name = 'followuplink.html'
    model = Communication

    def get_context_data(self, **kwargs):
        context = super(CrmFollowUpView, self).get_context_data(**kwargs)
        context['followups'] = Communication.objects.filter(
            next_followup__date=datetime.today())
        context['followup_count'] = Communication.objects.filter(
            next_followup__date=datetime.today()).count()
        return context


class CommunicationView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        print "I am here"
        contact = Contact.objects.get(pk=self.kwargs.get('pk'))
        form = CommunicationForm(request.POST)
        print "++++++"
        print form
        print "++++++"
        print 'i m sloved'
        if form.is_valid():
            instance = form.instance
            instance.contact = contact
            instance.user = self.request.user
            instance.save()
            print 'i m valid form'
            form.save()
            print 'i m saved'
            messages.success(
                request, 'Well done!Your communication is Addded Succesfully.')
        else:
            print form.errors
            messages.warning(
                request, form.errors)
        return HttpResponseRedirect(
            '/crm/detail/{0}/'.format(contact.id))


class DeleteCommunicationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        Communication.objects.latest('created_at').delete()
        contact = Contact.objects.get(pk=self.kwargs.get('pk'))
        messages.success(
            request, 'Well done!Your item is removed Succesfully.')
        return HttpResponseRedirect(
            '/crm/detail/{0}/'.format(contact.id))


class HotView(PermissionRequiredMixin, ListView):
    template_name = 'hot.html'
    model = Contact

    permission_required = 'auth.add_user'

    def get_context_data(self, **kwargs):
        context = super(HotView, self).get_context_data(**kwargs)
        context['hot_count'] = Contact.objects.filter(status=3).count()
        context['hot_followup'] = Contact.objects.filter(status=3)
        return context


class ProposedView(PermissionRequiredMixin, ListView):
    template_name = 'proposed.html'
    model = Contact

    permission_required = 'auth.add_user'

    def get_context_data(self, **kwargs):
        context = super(ProposedView, self).get_context_data(**kwargs)
        context['proposed_count'] = Contact.objects.filter(status=5).count()
        context['proposed_folloup'] = Contact.objects.filter(status=5)
        return context


class ProposalPendingView(PermissionRequiredMixin, ListView):
    template_name = 'proposed_pending.html'
    model = Contact
    permission_required = 'auth.add_user'

    def get_context_data(self, **kwargs):
        context = super(ProposalPendingView, self).get_context_data(**kwargs)
        context['proposal_count'] = Contact.objects.filter(status=9).count()
        context['pending_proposed_folloup'] = Contact.objects.filter(status=9)
        return context


class UrlDispatchView(LoginRequiredMixin, TemplateView):

    def get(self, *args, **kwargs):

        try:
            groups = self.request.user.groups.all()
            groups = [group.name for group in groups]
        except:
            raise Http404(
                "User is not assigned to any group, Please assign and Try again")

        if 'sales' or 'admin' in groups:
            return HttpResponseRedirect(reverse('crm:list'))
        else:
            return HttpResponseRedirect(reverse('ticket:list'))


@login_required
def change_password(request):
    username = request.user.username
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            request.user.set_password(request.POST['password1'])
            request.user.save()
            messages.success(request, "Password reset successful ")
            return HttpResponseRedirect("/crm/")
        else:
            messages.success(request, "Try again Error Password did not match")
            return render(request, 'change_password.html', {'username':username})
    else:
        return render(request, 'change_password.html', {'username':username})
