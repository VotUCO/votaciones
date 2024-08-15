from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from voting.models import Voting, AuthorizedUsers
from voting.api.serializers import AuthorizedUserSerializer, UserVotingSerializer
from rest_framework.permissions import IsAuthenticated

class PublicVotingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        votings = UserVotingSerializer(Voting.objects.filter(privacy=False, 
                                                             start_date__lt=timezone.now(),
                                                             end_date__gt=timezone.now()), 
                                                             many=True)
        return Response(status=status.HTTP_200_OK, data=votings.data)

