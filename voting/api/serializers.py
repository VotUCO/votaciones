from rest_framework.serializers import ModelSerializer
from voting.models import Voting, AuthorizedUsers

class UserVotingSerializer(ModelSerializer):
    class Meta:
        model = Voting
        fields = ['id', 'name', 'voting_system', 'start_date', 'end_date']

class AuthorizedUserSerializer(ModelSerializer):
    class Meta:
        model = AuthorizedUsers
        fields = ['voting_id', 'user']

class VotingSerializer(ModelSerializer):
    class Meta:
        model = Voting
        fields = ['id', 'name', 'voting_system', 'start_date', 'end_date']
