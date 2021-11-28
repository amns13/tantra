from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_calss = RegistrationSerializer

    def post(self, request: Request) -> Response:
        user = request.data

        serializer = self.serializer_calss(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
