from django.http import Http404
from django.contrib import admin
from .models import ColdCallContact, Communication
from crm.models import Contact


class Communicationline(admin.TabularInline):
    model = Communication
    extra = 1


class ColdCallContactAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'user__username']
    list_display = [
        'company_name', 'contact_name', 'ph_number1', 'email', 'status',
        'category', 'user', 'created_at', 'updated_at', 'remark']
    ordering = ('-updated_at',)
    date_hierarchy = 'updated_at'
    empty_value_display = '-empty-'
    list_filter = ('status', 'created_at', 'user')
    actions = ['move_to_contact']
    inlines = [Communicationline]

    class Meta:
        model = ColdCallContact

    def move_to_contact(self, request, queryset):
        try:
            for obj in queryset:
                Contact.objects.create(
                    contact_name=obj.contact_name,
                    company_name=obj.company_name, status=2,
                    bio=obj.bio, ph_number1=obj.ph_number1,
                    email=obj.email)
        except:
            raise Http404
    move_to_contact.short_description = "Move selected contacts"


admin.site.register(ColdCallContact, ColdCallContactAdmin)
