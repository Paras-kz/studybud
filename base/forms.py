from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model=Room
        #i.e the name of model for which we are creating this room
        fields="__all__"
        exclude=['host','participants']
