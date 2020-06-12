from django.contrib import admin
from .models import Resource

class ResourceAdmin(admin.ModelAdmin):
    #Fields we want to show in the Listing
    list_display = ('id', 'name', 'resource_type', 'language', 'is_published', 'version','size','filename')
    list_display_links = ('id', 'name',) # clickable element to access object
    list_filter = ('language','resource_type',) #Filter box to filter by
    list_editable = ('is_published',) # Edit field on the Table Row itself
    #Fields we'll use to search in the search box
    search_fields = ('name', 'language', 'resource_type',)
    exclude = ('size','filename',)
    readonly_fields=('version',)
    list_per_page = 25


# Register your models here.
admin.site.register(Resource, ResourceAdmin)

