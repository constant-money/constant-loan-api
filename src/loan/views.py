from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SampleAuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response()


class VerifyPhone(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        obj = ExchangeUser.objects.get(user=request.user)

        phone_number = request.data.get('phone_number')
        if not phone_number:
            raise ValidationError