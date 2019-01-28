from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SampleAuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        print(request.user.email)
        return Response()
