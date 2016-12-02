from django.contrib import admin
from .models import Contact, Communication


class Communicationline(admin.TabularInline):
    model = Communication
    extra = 1


class ContactAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'status']
    list_display = [
        'company_name', 'status', 'ph_number1', 'total_communications',
        'next_followup_date', 'created_at', 'updated_at']
    fieldsets = [
        ('Overview:', {'fields': ['company_name', 'contact_name',
                                  'status', 'ph_number1',
                                  'email', 'bio', 'group'
                                  ]}),
        ('Other:', {'fields': ['addressline1', 'addressline2',
                               'zipcode', 'city',
                               'state', 'country'],
                    'classes': ['collapse']}),
    ]
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'
    list_filter = ('status', 'created_at', 'updated_at')
    inlines = [Communicationline]

    class Meta:
        model = Contact

admin.site.register(Contact, ContactAdmin)
