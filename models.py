from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from crm.models import TimeStamp

STATUS = (
    (1, 'Contacted'),
    (2, 'Not-Contacted'),
    (3, 'Moved to crm'),
)

Category = (
    (1, 'Tool Room'),
    (2, 'Auto-Service'),
    (3, 'Billing'),
    (4, 'Injection moulding'),
    (5, 'Sheet metal components'),
    (6, 'Flexible Packaging and Printing'),
)

Response = (
    (1, 'Soft'),
    (2, 'Medium'),
    (3, 'Hard'),
)

COMMUNICATIONTYPE = (
    (1, 'Phone'),
    (2, 'E-Mail'),
    (3, 'SMS'),
)


class ColdCallContact(TimeStamp):
    contact_name = models.CharField(
        'Contact Name',
        max_length=50, blank=True)
    company_name = models.CharField(
        'Company Name',
        max_length=50, unique=True)
    bio = models.TextField(max_length=2000, blank=True)
    ph_number1 = models.CharField(
        max_length=50,
        blank=True, verbose_name=_("Phone No."))
    email = models.EmailField(
        max_length=254, verbose_name=_("E-Mail"), blank=True)
    status = models.IntegerField(
        default=2,
        choices=STATUS,
        help_text="'Contacted':If contacted and not interested."
        "'Not-Contacted':If not contacted"
        "'Moved to crm':If interested for demo and moved to crm")
    user = models.ForeignKey(User, null=True)
    category = models.IntegerField(
        choices=Category,
        help_text="'Tool Room': related to tool room."
        "'Auto-Service': related to Car/Bike service product."
        "'Billing': related to accounts/billing product"
        "'Injection moulding': related to plastic components manufacturing"
        "'Sheet metal components': related to hydraulic press"
        "'Flexible Packaging and Printing': related to packaging and printing industry")
    website = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    response = models.IntegerField(
        blank=True, null=True,
        choices=Response,
        help_text="'Soft':Responded gently with motivational talks."
        "'Medium':Responded in general."
        "'Hard':Rude behaviour")
    group = models.ForeignKey(Group, null=True)

    def __unicode__(self):
        return self.company_name

    def next_followup_date(self):
        try:
            return self.communication_set.last().next_followup
        except:
            return None

    class Meta:
        ordering = ['-updated_at']


class Communication(TimeStamp):
    coldcallcontact = models.ForeignKey(ColdCallContact)
    type_of_communication = models.IntegerField(
        choices=COMMUNICATIONTYPE, default=1)
    remark = models.CharField(max_length=500, blank=True, null=True)
    next_followup = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Write your code here
        self.coldcallcontact.save()
        super(Communication, self).save(*args, **kwargs)
