from django.contrib import admin
from .models import Contact, Newsletter

admin.site.register(Contact)
admin.site.register(Newsletter)

# customize admin panel 
admin.site.site_header = "EASI Admin Panel"
admin.site.site_title = "EASI Admin Panel"
admin.site.index_title = "Welcome to EASI Admin Panel"

