from django.contrib import admin

# Register your models here.
from .models import RequestTable
    
class requestAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'module', 'owner', 'request_duration', 'submit_date')

admin.site.register(RequestTable, requestAdmin)