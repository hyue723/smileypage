from django.contrib import admin
from .models import Event, Profile, Friend, FriendshipRequest

admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(FriendshipRequest)


