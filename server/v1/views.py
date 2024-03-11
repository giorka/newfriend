from rest_framework import views


class RegisterAPIView(views.APIView):
    def post(self, request) -> views.Response:
        ...
