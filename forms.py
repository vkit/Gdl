from django import forms
from .models import Ticket, TicketComment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('project', 'title', 'body', 'file')


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ('body',)


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', ]
