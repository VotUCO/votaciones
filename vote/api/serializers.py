from vote.models import Vote
from rest_framework.serializers import ModelSerializer

from voting.models import Voting, Options


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ['token', 'voting_date', 'voting_id']

class VotingSerializer(ModelSerializer):
    class Meta:
        model = Voting
        fields = ['id', 'name']

class VotingAdminSerializer(ModelSerializer):
    class Meta:
        model = Voting
        fields = ['id', 'name', 'privacy']

class OptionSerializer(ModelSerializer):
    class Meta:
        model = Options
        fields = ['name']