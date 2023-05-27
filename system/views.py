
from rest_framework import viewsets, status
from rest_framework.views import APIView
# from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken


from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import (
    ImageSerializer,
    LanguageSerializer,
)
from .models import (
    Language,
    Image
)

# Create your views here.


class LanguageView(viewsets.ModelViewSet):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]


class ImageListView(APIView):
    # authentication_classes = [JWTAuthentication]
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self,request,format=None):
        try:
            # user = request.user
            images = Image.objects.all()
            serializer = ImageSerializer(images,many=True)
            # print(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class ImageView(APIView):
    # authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request,image_id,format=None):
        image = get_object_or_404(Image,id=image_id)
        try:
            # user = request.user
            serializer = ImageSerializer(image)
            # print(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
