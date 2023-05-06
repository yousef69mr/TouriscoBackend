
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import (
    
    LanguageSerializer,
)
from .models import (
    Language,
    
)

# Create your views here.


class LanguageView(viewsets.ModelViewSet):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]


