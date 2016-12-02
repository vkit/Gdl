from django import forms
from .models import Contact, Communication


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('contact_name', 'company_name', 'status', 'bio', 'email', 'addressline1', 'addressline2', 'zipcode', 'city', 'state', 'country', 'ph_number1', 'ph_number2')


class CommunicationForm(forms.ModelForm):
        class Meta:
            model = Communication
            fields = (
                'type_of_communicaiton', 'direction', 'remark', 'next_followup')


class ContactUpdateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('contact_name', 'company_name', 'status', 'bio', 'email', 'addressline1', 'addressline2', 'zipcode', 'city', 'state', 'country', 'ph_number1', 'ph_number2')


class CommunicationUpdateForm(forms.ModelForm):
        class Meta:
            model = Communication
            fields = (
                'type_of_communicaiton', 'direction', 'remark', 'next_followup') 


class DeleteCommForm(forms.ModelForm):
        class Meta:
            model = Communication
            fields = (
                'type_of_communicaiton', 'direction', 'remark', 'next_followup')                    

 