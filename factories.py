from factory.django import DjangoModelFactory
from ticket.models import Ticket, TicketComment
from django.contrib.auth.models import User
import factory
from django.utils import timezone


class UserFactory(DjangoModelFactory):
    class Meta:
        model = Ticket
    username = factory.Sequence(lambda n: "username%d" % n)
    password = 'greendisgn123'
    email = 'rao.raghavendra41@gmail.com'


class TicketFactory(DjangoModelFactory):
    class Meta:
        model = TicketComment
    post = factory.SubFactory(UserFactory)
    name = 'green design'
    email = 'rao.raghavendra41@gmail.com'
    body = 'good yar'
 