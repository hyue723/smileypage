from django.contrib import admin
from .models import Event, Profile, Connection, HelpRequest

admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Connection)
admin.site.register(HelpRequest)


