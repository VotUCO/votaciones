from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from voting.models import Voting, AuthorizedUsers
from voting.api.serializers import AuthorizedUserSerializer, UserVotingSerializer
from rest_framework.permissions import IsAuthenticated

class PrivateVotingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        authorized_votings = AuthorizedUserSerializer(AuthorizedUsers.objects.filter(user=request.GET['user']), many=True)
        votings_id = []
        for voting in authorized_votings.data:
            votings_id.append(voting['voting_id'])
        votings = UserVotingSerializer(Voting.objects.filter(id__in=votings_id, end_date__lt=timezone.now(), start_date__gt=timezone.now()), many=True)
        return Response(status=status.HTTP_200_OK, data=votings.data)

