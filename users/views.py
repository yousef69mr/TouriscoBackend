from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
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
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdminUser]


class CreateUserView(APIView):
    
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)



class ActiveUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = get_object_or_404(User,id=request.user.id)
        try:
            serializer = UserSerializer(user)
            return Response(serializer.data,status=status.HTTP_302_FOUND)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)