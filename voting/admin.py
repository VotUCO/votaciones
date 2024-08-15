from django.contrib import admin
from voting.models import Voting, AuthorizedUsers

# Register your models here.
@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state', 'privacy', 'start_date', 'voting_creator']

@admin.register(AuthorizedUsers)
class AuthorizedUsersAdmin(admin.ModelAdmin):
    list_display = ['voting_id', 'user']