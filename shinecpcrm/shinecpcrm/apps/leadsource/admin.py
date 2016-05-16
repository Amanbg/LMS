from django.contrib import admin

# # Register your models here.
from leadsource.models import LeadSource


class LeadSourceAdmin(admin.ModelAdmin):

    fieldsets = ('Source details', {
                  'fields': ('source_name', 'status')
                }),
    list_display = ['source_name', 'status']
    list_filter = ["source_name"]


admin.site.register(LeadSource, LeadSourceAdmin)
