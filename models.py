from __future__ import unicode_literals
# import uuid

from django.utils.translation import ugettext_lazy as _

from django.db import models

from django.contrib.auth.models import User, Group


class TimeStamp(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


STATUS = (
    (1, 'Luke-Warm'),
    (2, 'Warm'),
    (3, 'Hot'),
    (4, 'Dead'),
    (5, 'Proposed'),
    (6, 'Closed'),
    (7, 'Inactive'),
    (8, 'Proposed and Inactive'),
    (9, 'Proposal Pending'),
)


class Contact(TimeStamp):

    contact_name = models.CharField(
        'Contact Name',
        max_length=50, blank=True)
    company_name = models.CharField(
        'Company Name',
        max_length=50, unique=True)
    bio = models.TextField(max_length=2000, blank=True)
    # pan_no = models.CharField(max_length=50, blank=True)
    # tin_no = models.CharField(max_length=50, blank=True)
    # service_tax_no = models.CharField(max_length=50, blank=True)
    # payment_terms = models.CharField(max_length=100, blank=True)
    status = models.IntegerField(
        choices=STATUS,
        help_text="'Luke-warm': vaguely interested"
        "'Warm': Got a requirment, Lightly interested or enthusiastic "
        "about our product"
        "'Hot': Got a requirment and greatly interested"
        "'Dead': No more intersted or Already procured from some else"
        "'Inactive': Not responding or Need some more time and follow"
    )
    ph_number1 = models.CharField(
        max_length=50,
        blank=True, verbose_name=_("Phone No."))
    ph_number2 = models.CharField(
        max_length=50, blank=True, verbose_name=_("Alternate No."))
    addressline1 = models.CharField(
        max_length=200, verbose_name=_("Addressline 1"), blank=True)
    addressline2 = models.CharField(
        max_length=200, verbose_name=_("Addressline 2"), blank=True)
    email = models.EmailField(
        max_length=254, verbose_name=_("E-Mail"), blank=True)
    zipcode = models.IntegerField(
        verbose_name=_("Zipcode"), blank=True, null=True)
    city = models.CharField(
        max_length=100, verbose_name=_("City"), blank=True)
    state = models.CharField(
        max_length=100, verbose_name=_("State"), blank=True)
    country = models.CharField(
        max_length=50, verbose_name=_("Country"), blank=True)
    group = models.ForeignKey(Group, null=True)

    def __unicode__(self):
        return self.company_name

    def next_followup_date(self):
        try:
            return self.communication_set.last().next_followup
        except:
            return None

    def total_communications(self):
        return self.communication_set.count()

    class Meta:
        ordering = ['-updated_at']


COMMUNICATIONTYPE = (
    (1, 'Phone'),
    (2, 'E-Mail'),
    (3, 'Personal Meeting'),
    (4, 'SMS'),
)

DIRECTION = (
    (1, 'Outgoing'),
    (2, 'Incoming'),
)


class Communication(TimeStamp):
    contact = models.ForeignKey(Contact, null=True, blank=True)
    type_of_communicaiton = models.IntegerField(choices=COMMUNICATIONTYPE)
    direction = models.IntegerField(choices=DIRECTION, default=1)
    remark = models.CharField(max_length=500)
    next_followup = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.remark

    def save(self, *args, **kwargs):
        # Write your code here
        self.contact.save()
        super(Communication, self).save(*args, **kwargs)

