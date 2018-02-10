from django.contrib.auth.models import Permission, User
from django.db import models
import datetime
from django.utils import timezone

class Profile(models.Model):
    UNDERGRADUATE = "Undergraduate Student"
    GRADUATE="Graduate Student"
    STAFF="Staff"
    NONCMU='No in Cmu'
    PROFESSOR='Professor'
    STATUS_CHOICES = (
    (UNDERGRADUATE,"Undergraduate Student"),
    (GRADUATE,"Graduate Student"),
    (PROFESSOR, 'Professor'),
    (STAFF,"School Staff"),
    (NONCMU,'Not in CMU'),
    )
    status_in_cmu = models.CharField( max_length=100,
                                      choices=STATUS_CHOICES,
                                      default=UNDERGRADUATE)
    user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE, 
        related_name='profile_user')
    interest = models.CharField(max_length = 500)
    profile_photo=models.FileField()
    studying_fields=models.CharField(max_length=500)
    facebook_page=models.URLField(blank = True, null=True)
    friends = models.ManyToManyField(User, related_name="profile_friends")


class Event(models.Model):
    FOOD='Food'
    STUDY='Study'
    OTHER='Other'
    KIND_CHOICES=(
        (FOOD,'Food'),
        (STUDY,'Study'),
        (OTHER,'Other'),
        )
    user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE, 
        related_name = "event_creator")
    name = models.CharField(max_length = 500)
    kind = models.CharField(max_length=100, choices=KIND_CHOICES, default=FOOD)
    end_time = models.TimeField(default = datetime.datetime.now) 
    start_time = models.TimeField(default = datetime.datetime.now) 
    date = models.DateField(default = datetime.date.today)
    location = models.CharField(max_length = 500)
    description = models.TextField()
    event_photo=models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name + "at" + self.location


class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(User, default = 1,on_delete = models.CASCADE, 
        related_name="FriendshipRequest_user1")
    to_user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE,
        related_name="FriendshipRequest_user2")

    message = models.TextField(blank=True, null = True)

    created = models.DateTimeField(default=datetime.datetime.now)
    rejected = models.BooleanField(default = False)
    viewed = models.BooleanField(default = False)
    accepted = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'Friendship Request'
        verbose_name_plural = 'Friendship Requests'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%d friendship requested #%d" % (self.from_user_id, 
            self.to_user_id)


class Friend(models.Model):
    """ Model to represent Friendships """
    to_user = models.ForeignKey(User,default = 1, on_delete = models.CASCADE,
        related_name="Friend_user1")
    from_user = models.ForeignKey(User, default = 1,on_delete = models.CASCADE,
        related_name="Friend_user2")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%d is friends with #%d" % (self.to_user_id, 
            self.from_user_id)



