from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from voting.models import Voting, AuthorizedUsers
from voting.api.serializers import UserVotingSerializer, VotingSerializer
import ast

class VotingAPIView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = VotingSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        voting = serializer.save()
        if request.POST['privacy'] == 'True':
            authorized_users = ast.literal_eval(request.POST['authorized_users'])
            print(authorized_users)
            for user in authorized_users:
                auth_user = AuthorizedUsers.objects.create(voting_id=voting,
                                               user=user)
                auth_user.save()
        
        return Response(status=status.HTTP_200_OK, data=UserVotingSerializer(voting, many=False).data)

    def patch(self, request):
        s