from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from .serializers import RegistrationSerializer
from .models import User


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_calss = RegistrationSerializer

    def post(self, request: Request) -> Response:
        user = request.data

        serializer = self.serializer_calss(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        created_user: User = serializer.instance
        email_token = created_user.send_email_verification_email()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailVerificationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, token: str) -> Response:
        user = User.verify_email_verification_token(token)
        if user:
            user.is_verified = True
            user.save()
            context = {'message': _("User account verified.")}
            return Response(data=context, status=status.HTTP_200_OK)

        return Response(_("User data not found."),
                        status=status.HTTP_404_NOT_FOUND)
