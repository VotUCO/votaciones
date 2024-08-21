from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "No se ha proporcionado un usuario activo válido"})
        else:
            return bool(request.user and request.user.rol == "admin")
