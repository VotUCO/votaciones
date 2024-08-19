from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from voting.models import Voting, AuthorizedUsers
from voting.api.serializers import UserVotingSerializer, VotingSerializer
from rest_framework.authtoken.models import Token
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
    
    def put(self, request):
        voting = Voting.objects.filter(id=request.PUT["id"])
        token = Token.objects.get(key=request.META.get["HTTP_AUTHORIZATION"])
        user_id = token.user_id
        if VotingSerializer(voting, many=False).data.get("voting_creator") == user_id:
            if VotingSerializer(voting, many=False).data.get("state") == False:
                voting_modified = VotingSerializer(voting, data=request.PUT)
                voting_modified.save()
            return Response(status=status.HTTP_403_FORBIDDEN, data='{"error": "No se puede modificar una votación ya publicada"}')
        return Response(status=status.HTTP_403_FORBIDDEN, data='{"error": "No se puede modificar una votación de la que no es creador"}')
    
    def delete(self, request):
        token = Token.objects.get(key=request.META.get["HTTP_AUTHORIZATION"])
        user_id = token.user_id
        voting = VotingSerializer(Voting.objects.filter(id=request.DELETE["id"]), many=False)
        if voting:
            if voting.data.voting_creator == user_id:
                if voting.data.status == True:
                    Voting.objects.filter(id=request.DELETE["id"]).delete()
                    return Response(status=status.HTTP_200_OK, data='{"detail": "La votación se ha eliminado"}}')
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN, data='{"error": "No se puede eliminar una votación que ya está publicada"}')
            else:
                return Response(status=status.HTTP_403_FORBIDDEN, data='{"error": "No se puede eliminar una votación de la que no se es propietario"}')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data='{"error": "La votación no existe"}')
        
        