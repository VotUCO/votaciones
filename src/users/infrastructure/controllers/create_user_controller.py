import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from jinja2 import Template
from django.templatetags.static import static
from src.votaciones.settings import EMAIL_HOST_USER

from src.users.application.user_creator import UserCreator
from src.users.infrastructure.builders.user_builder import UserBuilder
from src.users.infrastructure.mysql_user_repository import MySQLUserRepository
from src.users.infrastructure.serializers.user_serializer import UserSerializer


class CreateUserController(APIView):
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user_builder = UserBuilder()
        self.__user_serializer = UserSerializer()
        self.__user_repository = MySQLUserRepository(self.__user_builder)
        self.__user_creator = UserCreator(self.__user_repository)

    def post(self, request: Request) -> Response:
        user = self.__user_builder.build(json.loads(request.body))
        user_created = self.__user_creator.create(user)
        template_email = """<!DOCTYPE html>
			<html lang="en">
			  <head>
			    <meta charset="UTF-8" />
			    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
			    <title>Register Email VotUCO</title>
			    <style>
			      img {
				width: 250px;
			      }
			      .container {
				display: block;
				margin: 20px;
			      }
			      .containterimage {
				display: flex;
				justify-content: center;
			      }
			      p {
				font-family: Verdana, Geneva, Tahoma, sans-serif;
				margin-bottom: 30px;
			      }
			      footer {
				font-family: Verdana, Geneva, Tahoma, sans-serif;
				font-size: 12px;
			      }
			    </style>
			  </head>
			  <body>
			    <main>
			      <div class="container">
				<div class="containterimage">
				  <img
				    alt="Logo VotUCO"
				    src="http://jesusescribano.net/logovotuco.png"
				    style="justify-content: center"
				  />
				</div>
				<p>
				  ¡Bienvenid@ a VotUCO {{ nombre }}! A partir de ahora puedes acceder al
				  dashboard principal de la aplicación
				  <a href="https://jesusescribano.net/">desde aquí</a>
				</p>
				<p>¡Muchas gracias por el registro!</p>
			      </div>
			    </main>
			    <footer>Este email es para: {{ email }}</footer>
			  </body>
			</html>"""
        jinja_template = Template(template_email)
        email_data = {
            "subject": "Confirmación de Registro en VotUCO",
            "nombre": user_created.name,
            "email": user_created.email,
        }
        mail = jinja_template.render(email_data)

        email = EmailMultiAlternatives(
            subject="Confirmación de Registro en VotUCO",
            from_email=f"VotUCO Sistema de Votaciones <{EMAIL_HOST_USER}>",
            to=[user_created.email],
        )
        email.attach_alternative(mail, "text/html")
        email.send()
        return Response(
            status=status.HTTP_200_OK,
            data={"success": self.__user_serializer.serialize(user_created)},
        )
