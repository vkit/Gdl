from django import forms
from .models import ColdCallContact, Communication


class ColdCallContactForm(forms.ModelForm):
    class Meta:
        model = ColdCallContact
        fields = ('contact_name', 'company_name', 'bio',
                  'ph_number1', 'email', 'status', 'category',
                  'website', 'remark', 'response')


class CommunicationForm(forms.ModelForm):
        class Meta:
            model = Communication
            fields = (
                'type_of_communication', 'remark', 'next_followup')


class ColdCallContactUpdateForm(forms.ModelForm):
    class Meta:
        model = ColdCallContact
        fields = ('contact_name', 'company_name', 'bio',
                  'ph_number1', 'email', 'status', 'category',
                  'website', 'remark', 'response')

