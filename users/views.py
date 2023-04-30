from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView

from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
# from system.models import invertedIndex
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # print(invertedIndex())
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CreateUserView(APIView):
    # permission_classes=[AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):

    def get(self, request):
        pass
