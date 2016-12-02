from django.contrib import admin

from .models import Ticket, TicketComment


class TicketInline(admin.TabularInline):
    model = Ticket


class TicketCommentInline(admin.TabularInline):
    model = TicketComment


class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'created', 'created_by',
        'ticket_id', 'body',
        'status', 'updated', 'file')
    date_hierarchy = 'created'
    list_filter = ['created']
    inlines = [
        TicketCommentInline,
    ]


admin.site.register(Ticket, TicketAdmin)






