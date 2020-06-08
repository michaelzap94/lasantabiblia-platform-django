from django.contrib import admin
# Import the DEFAULT User admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Convert string in our python to Human readable code.
# Also useful to translate to different languages.
from django.utils.translation import gettext as _
from .models import Account

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'firstname', 'lastname', 'date_joined', 'last_login', 'is_admin','is_staff']
    search_fields = ('email','firstname', 'lastname')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    # SUPPORT our CUSTOM User Model
    # Defines the fields and sections that you see for EACH user.
    # Structure: Title for the sections | fields it will contain
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('firstname','lastname')}),
        (_('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
        }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    # django: built-in ->
    # -> Defines the fields that you include on the add page(create user page)
    # Structure: Title for the sections | fields it will contain
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # built-in, default
            'fields': ('email', 'password1', 'password2')
        }),
    )

# Register our custom Account model to SHOW UP in the django Admin
admin.site.register(Account, UserAdmin)

