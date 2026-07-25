from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/accounts/register/ — anyone can create an account."""
    queryset = None
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    """GET /api/accounts/me/ — returns the logged-in user's own profile."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)