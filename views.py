from .models import ColdCallContact, Communication
from django.views.generic import ListView, DetailView, View
from .forms import ColdCallContactForm, CommunicationForm, ColdCallContactUpdateForm
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from base.views import GenericSelfRedirection, GenericModalUpdateView
from crm.models import Contact
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.contrib.auth.models import Group


class ColdCallContactView(ListView):
    template_name = 'coldcall_list.html'
    model = ColdCallContact

    def get_context_data(self, **kwargs):
        context = super(ColdCallContactView, self).get_context_data(**kwargs)
        context['form'] = ColdCallContactForm()
        context['user'] = self.request.user
        try:
            groups = self.request.user.groups.all()
            groups = [group.name for group in groups]
        except:
            raise Http404(
                "User is not assigned to any group,Please assign and Try again")
        if 'sales' in groups:
            groups.remove('sales')
            context['coldcallcontacts'] = [
                coldcall for coldcall in ColdCallContact.objects.filter(
                    group__name=groups[0])]
        else:
            context['coldcallcontacts'] = ColdCallContact.objects.all()
        return context


class ModalCreateView(
    PermissionRequiredMixin,
    GenericSelfRedirection
):
    form_class = ColdCallContactForm
    object_name = 'ColdCallContact'
    permission_required = 'crm.add_crm'
    url_pattern_list = ['coldcall', 'detail']
    error_url = '/coldcall/coldlist/'


class ColdCallContactDetailView(DetailView):
    template_name = 'cold_detail.html'
    model = ColdCallContact

    def get_context_data(self, **kwargs):
        context = super(
            ColdCallContactDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['coldcallcontact'] = ColdCallContact.objects.get(
            pk=self.kwargs.get('pk'))
        context['form'] = CommunicationForm()
        context['form1'] = ColdCallContactUpdateForm(
            instance=context['coldcallcontact'])
        return context


class ColdCallContactUpdateView(
    PermissionRequiredMixin, GenericModalUpdateView
):

    permission_required = 'crm.add_crm'
    form_class = ColdCallContactUpdateForm
    object_name = 'ColdCallcontact'
    model = ColdCallContact
    app_url = '/coldcall/'
    page_url = '/detail/'

    def get_success_url(self):
        return '/coldcall/detail/{0}'.format(self.kwargs.get('pk'))


class CommunicationView(View):

    def post(self, request, *args, **kwargs):
        print "I am here"
        coldcallcontact = ColdCallContact.objects.get(pk=self.kwargs.get('pk'))
        form = CommunicationForm(request.POST)
        print "++++++"
        print form
        print "++++++"
        print 'i m sloved'
        if form.is_valid():
            instance = form.instance
            instance.coldcallcontact = coldcallcontact
            instance.save()
            print 'i m valid form'
            form.save()
            print 'i m saved'
            messages.success(
                request, 'Well done!Your message is Addded Succesfully.')
        else:
            print form.errors
            messages.warning(
                request, form.errors)
        return HttpResponseRedirect(
            '/coldcall/detail/{0}/'.format(coldcallcontact.id))


class MoveToCrmView(View):

    def post(self, request, *args, **kwargs):
        for_action = request.POST.getlist('for_action')
        print "++++++"
        print "+++++++"
        print for_action
        print "+++++++"
        objs = ColdCallContact.objects.filter(pk__in=for_action)
        print "++++++"
        print objs
        print "+++++++"
        if len(objs) == 0:
            msg = "select atleast one object"
            messages.warning(request, msg)
        else:
            try:
                for obj in objs:
                    obj.status = 3
                    Contact.objects.create(
                        contact_name=obj.contact_name,
                        company_name=obj.company_name, status=2,
                        bio=obj.bio, ph_number1=obj.ph_number1,
                        email=obj.email, group=obj.group
                    )
                    obj.save()
                messages.success(
                    request, 'Well done!Your contact is moved Succesfully.')
            except:
                messages.warning(
                    request, 'Selected contacts already moved.')
        return HttpResponseRedirect('/coldcall/coldlist/')


class DeletecoldcallCommunicationView(View):

    def get(self, request, *args, **kwargs):
        a = Communication.objects.latest('created_at')
        try:
            if a is not None:
                a.delete()
                coldcallcontact = ColdCallContact.objects.get(pk=self.kwargs.get('pk'))
                messages.success(
                    request, 'Well done!Your item is removed Succesfully.')
                return HttpResponseRedirect(
                    '/coldcall/detail/{0}/'.format(coldcallcontact.id))
        except:
            messages.warning(
                request, 'No data to delete.')
            return HttpResponseRedirect(
                '/coldcall/detail/{0}/'.format(coldcallcontact.id))

