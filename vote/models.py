import secrets
from django.db import models
from django.utils import timezone

# Create your models here.
class Vote(models.Model):
    token = models.CharField(primary_key=True, max_length=500, null=False, editable=False, default=secrets.token_hex(16))
    vote = models.JSONField()
    voting_date = models.DateTimeField(editable=False, default=timezone.now)
    voting_id = models.UUIDField(null=False)

