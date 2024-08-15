from django.utils import timezone
import uuid
from django.db import models

# Create your models here.
class Voting(models.Model):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    name = models.CharField(max_length=300)
    state = models.BooleanField(default=False)
    voting_system = models.CharField(max_length=200)
    privacy = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    voting_creator = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Options(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name = 'option')
    name = models.CharField(max_length=255)

class AuthorizedUsers(models.Model):
    voting_id = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='authorized_user')
    user = models.CharField(max_length=255)
