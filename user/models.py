from django.contrib.auth.models import Permission, User
from django.db import models
import datetime
from django.utils import timezone
# when ever you change things in models, makemigration and migrate

class Profile(models.Model):
    MEDICALSTAFF = "Medical Staff"
    PATIENT="Patient"
    STATUS_CHOICES = (
    (MEDICALSTAFF, "Medical Staff"),
    (PATIENT, "Patient"),
    )
    status = models.CharField( max_length=100,
                                      choices=STATUS_CHOICES,
                                      default=PATIENT)

    user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE, 
        related_name='profile_user')
    birthday = models.DateField(default = datetime.date.today)
    location = models.CharField(max_length = 100, default = '')
    profile_photo = models.FileField()
    radius = models.PositiveIntegerField(default = 1000) # in meters
    connections = models.ManyToManyField(User, related_name="profile_connections")



class Event(models.Model):
    # FOOD='Food'
    # STUDY='Study'
    # OTHER='Other'
    # KIND_CHOICES=(
    #     (FOOD,'Food'),
    #     (STUDY,'Study'),
    #     (OTHER,'Other'),
    #     )
    user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE, 
        related_name = "event_creator")
    symptoms = models.CharField(max_length = 500, default='')
    photo = models.FileField(default = '/static/images/bg-01.jpg')
    #kind = models.CharField(max_length=100, choices=KIND_CHOICES, default=FOOD)
    date = models.DateField(default = datetime.date.today)
    location = models.CharField(max_length = 100, default='')
    prediction = models.TextField(blank=True, null = True)

    def __str__(self):
        return self.name + "at" + self.location


class HelpRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(User, default = 1,on_delete = models.CASCADE, 
        related_name="HelpRequest_user1")
    to_user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE,
        related_name="HelpRequest_user2")

    message = models.TextField(blank=True, null = True)

    created = models.DateTimeField(default=datetime.datetime.now)
    rejected = models.BooleanField(default = False)
    viewed = models.BooleanField(default = False)
    accepted = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'Help Request'
        verbose_name_plural = 'Help Requests'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%d friendship requested #%d" % (self.from_user_id, 
            self.to_user_id)


class Connection(models.Model):
    """ Model to represent Friendships """
    to_user = models.ForeignKey(User,default = 1, on_delete = models.CASCADE,
        related_name="Connection_user1")
    from_user = models.ForeignKey(User, default = 1,on_delete = models.CASCADE,
        related_name="Connection_user2")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural = 'Connections'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%d is friends with #%d" % (self.to_user_id, 
            self.from_user_id)

