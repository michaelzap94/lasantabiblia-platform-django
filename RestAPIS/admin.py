from django.contrib import admin
from .models import Label, Verses_Marked, Verses_Learned
# Register your models here.
admin.site.register(Label)
admin.site.register(Verses_Marked)
admin.site.register(Verses_Learned)