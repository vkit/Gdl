from django.views.generic import ListView, View, DetailView
from .models import Ticket
from .forms import TicketForm, TicketCommentForm, TicketUpdateForm
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class TicketView(LoginRequiredMixin, ListView):
    template_name = 'ticket_list.html'
    model = Ticket
    login_url = '/ticket/'

    def get_context_data(self, **kwargs):
        context = super(TicketView, self).get_context_data(**kwargs)
        context['form'] = TicketForm()
        context['pending_count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='PENDING').count()
        context['solved_count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='SOLVED').count()
        context['reopened_count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='REOPENED').count()
        context['closed_count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='CLOSED').count()
        context['total_ticket'] = Ticket.objects.filter(
            created_by=self.request.user).count()
        context['posts'] = Ticket.objects.filter(
            created_by=self.request.user).order_by('-created')
        context['user'] = self.request.user
        print "I am heretoo"
        return context

    def post(self, request, *args, **kwargs):
        print "I am here"
        # check modal also put enctype="multipart/form-data" in
        # html for image
        form = TicketForm(request.POST, request.FILES)
        print "++++++"
        print form
        print "++++++"
        print 'i m sloved'
        if form.is_valid():
            instance = form.instance
            instance.created_by = self.request.user
            instance.save()
            print 'i m valid form'
            form.save()
            print 'form is saved'
            messages.success(request, 'Well done!Your Ticket is Addded Succesfully.')
        else:
            print form.errors
        return HttpResponseRedirect('/ticket/list/')


class TicketDetailView(DetailView):
    template_name = 'ticket_detail.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['form'] = TicketCommentForm()
        context['post'] = Ticket.objects.get(pk=self.kwargs.get('pk'))
        context['form1'] = TicketUpdateForm(instance=context['post'])
        return context


class TicketCommentView(View):

    def post(self, request, *args, **kwargs):
        form = TicketCommentForm(request.POST)
        if form.is_valid():
            instance = form.instance
            post = Ticket.objects.get(pk=self.kwargs.get('pk'))
            instance.post = post
            form.save()
            messages.success(
                request, 'Well done!Your Comment is Added Succesfully.')
            return HttpResponseRedirect(
                '/ticket/{0}/detail/'.format(self.kwargs.get('pk')))
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(
                '/ticket/{0}/detail/'.format(self.kwargs.get('pk')))


class TicketupdateView(View):

    def post(self, request, *args, **kwargs):
        post = Ticket.objects.get(pk=self.kwargs.get('pk'))
        print "++++++"
        print post
        print "++++++"
        form1 = TicketUpdateForm(request.POST, instance=post)
        if form1.is_valid():
            print 'I am form1 valid'
            form1.save()
            messages.success(
                request, 'Well done!Your status is updated succesfully.')
        else:
            print form1.errors
        return HttpResponseRedirect(
            '/ticket/{0}/detail/'.format(post.id))


class PendingTicketView(ListView):
    template_name = 'pending.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(PendingTicketView, self).get_context_data(**kwargs)
        context['count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='PENDING').count()
        context['pending_tickets'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='PENDING')
        return context


class SolvedTicketView(ListView):
    template_name = 'solved.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(SolvedTicketView, self).get_context_data(**kwargs)
        context['count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='SOLVED').count()
        context['solved_tickets'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='SOLVED')
        return context


class ReopenedTicketView(ListView):
    template_name = 'reopened.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(ReopenedTicketView, self).get_context_data(**kwargs)
        context['count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='REOPENED').count()
        context['reopened_tickets'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='REOPENED')
        return context


class ClosedTicketView(ListView):
    template_name = 'closed.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(ClosedTicketView, self).get_context_data(**kwargs)
        context['count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='CLOSED').count()
        context['closed_tickets'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='CLOSED')
        return context


class TotalStatusView(ListView):
    template_name = 'total.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(TotalStatusView, self).get_context_data(**kwargs)
        context['count'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='SOLVED').count()
        context['solved_tickets'] = Ticket.objects.filter(
            created_by=self.request.user).filter(status='SOLVED')
        return context
