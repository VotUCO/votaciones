from drf_yasg import openapi

name = openapi.Parameter('name', openapi.IN_BODY, description="The name of the voting proccess", type=openapi.TYPE_STRING)
state = openapi.Parameter('state', openapi.IN_BODY, description="If the voting process is published or draft", type=openapi.TYPE_BOOLEAN)
voting_system = openapi.Parameter('voting_system', openapi.IN_BODY, description="The voting system used in the voting process", type=openapi.TYPE_STRING)
privacy = openapi.Parameter('privacy', openapi.IN_BODY, description="The privacy of the voting: private (with authorized list) or public", type=openapi.TYPE_STRING)
start_date = openapi.Parameter('start_date', openapi.IN_BODY, description="The date where the voting starts", type=openapi.FORMAT_DATETIME)
end_date = openapi.Parameter('start_date', openapi.IN_BODY, description="The date where the voting ends", type=openapi.FORMAT_DATETIME)
