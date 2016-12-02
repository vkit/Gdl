from __future__ import unicode_literals

from django.db import models
from timetracking.models import Project
from django.contrib.auth.models import User

from django.utils import timezone


class TimeStamp(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        null=False)
    updated = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


CHOICE = (
    ('PENDING', 'PENDING'),
    ('SOLVED', 'SOLVED'),
    ('CLOSED', 'CLOSED'),
    ('REOPENED', 'REOPENED')
)


class Ticket(TimeStamp):
    project = models.ForeignKey(Project, null=True)
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User)
    ticket_id = models.IntegerField()
    body = models.TextField()
    status = models.CharField(
        max_length=40,
        choices=CHOICE, default='PENDING'
    )
    file = models.FileField(upload_to='documents/%Y/%m/%d', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            if Ticket.objects.last():
                tick = Ticket.objects.latest('created')
                self.ticket_id = tick.ticket_id + 1
            else:
                self.ticket_id = 1
        return super(Ticket, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class TicketComment(TimeStamp):

    post = models.ForeignKey(Ticket, null=True, blank=True)
    name = models.CharField(max_length=50)
    #date = models.DateTimeField(default=timezone.now)
    #email = models.EmailField()
    commented_by = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField()

    class Meta:
        def __unicode__(self):
            return self.name
