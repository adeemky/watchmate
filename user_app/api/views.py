from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistirationSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from user_app import models


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistirationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        else:
            data = serializer.errors

        return Response(serializer.data, status=status.HTTP_201_CREATED)


            # data["response"] = "Registration Successful!"
            # data["username"] = account.username
            # data["email"] = account.email
            # token = Token.objects.get(user=account).key
            # data['token'] = token
            # refresh'in yerine kullan