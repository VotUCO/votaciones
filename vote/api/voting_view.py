from vote.api.serializers import OptionSerializer, VoteSerializer, VotingAdminSerializer, VotingSerializer
from vote.models import Vote
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone


from voting.models import AuthorizedUsers, Options, Voting


class VotingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        voting_token = request.GET["token"]
        vote = VoteSerializer(Vote.objects.filter(token=voting_token), many=False)
        voting = VotingSerializer(Voting.objects.filter(id=vote.data.get("id")))
        data = {
            "token": vote.data.get("token"),
            "voting_date": vote.data.get("voting_date"),
            "vote": {
                "id": vote.data.get("id"),
                "name": voting.data.get("name"),
            }
        }
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request):
        token = Token.objects.get(key=request.META.get["HTTP_AUTHORIZATION"])
        user_id = token.user_id
        voting = VotingAdminSerializer(Voting.objects.filter(id=request.POST["voting_id"]), many=False)
        if voting.data.privacy == True:
            authorized = AuthorizedUsers.objects.filter(user=user_id, voting_id=voting.data.id)
            if not authorized:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data='{"error": "This user is unathorized for this voting"}') 
        options = OptionSerializer(Options.objects.filter(voting=voting.data.id), many=True)
        options_key = dict(request.POST["options"]).keys()
        options = list(options.data)

        options_key = set(options_key)
        options = set(options)

        if options_key == options:
            if voting.data.end_date < timezone.now() and voting.date.from_date > timezone.now():
                vote = Vote.objects.create(
                    vote=request.POST["options"],
                    voting_id=request.POST["voting_id"]
                )
                vote.save()
                return Response(status=status.HTTP_200_OK, data=VoteSerializer(vote, many=False).data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN, data='{"error": "La votación no está en fecha para votar"}')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='{"error": "Las opciones introducidas no son correctas"}')
