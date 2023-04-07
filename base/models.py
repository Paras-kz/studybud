from pyexpat import model
from unicodedata import name
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
# from base.views import room


# Create your models here.
class Topics(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    #We did not create user class as we have directly imported it
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #here aroom can have one topic but topic is related to many roomss
    topic=models.ForeignKey(Topics, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
     #host
    participants =models.ManyToManyField(User, related_name='participants',blank=True)
    #aboe line create a new entry in database named participants
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['-updated','-created']
        # '-updated' will maintain data in newest first

    def __str__(self):
        return self.name

class Messages(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering= ['-updated','-created']

    def __str__(self):
        return self.body[0:50]