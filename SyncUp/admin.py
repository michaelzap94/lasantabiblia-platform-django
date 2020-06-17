from django.contrib import admin
from .models import SyncUp

class SyncUpAdmin(admin.ModelAdmin):
    #Fields we want to show in the Listing
    list_display = ('id', 'user', 'version', 'last_device', 'updated')
    list_display_links = ('id', 'user',) # clickable element to access object
    readonly_fields=('updated',)
    list_per_page = 25


admin.site.register(SyncUp, SyncUpAdmin)
#admin.site.register(SyncUp)

