
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import (
    
    
    EventSerializer,
    EventsSerializer,
)
from .models import (
    LandmarkEvent,
    LandmarkEventLanguageBased
)

from system.models import Language
from landmarks.models import Landmark,LandmarkLanguageBased
from landmarks.serializers import LandmarksSerializer
# Create your views here.


class LandmarkEventListView(APIView):
    lookup_field = ['lang_code', 'landmark_id']

    # get events for specfic landmark
    def get(self, request, lang_code, landmark_id, format=None):

        language = get_object_or_404(Language, code=lang_code)
        landmark = get_object_or_404(Landmark, id=landmark_id)
        # events = LandmarkEvent.objects.filter(
        #     landmarkObject=landmark).only('id').all()
        lang_events = get_list_or_404(
            LandmarkEventLanguageBased, lang=language, eventObject__landmarkObject=landmark)
        # print(events)
        serializer = EventsSerializer(lang_events, many=True)

        return Response( serializer.data, status=status.HTTP_200_OK)


class LandmarkEventView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, landmark_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        landmark = get_object_or_404(Landmark, id=landmark_id)
        langlandmark = get_object_or_404(
            LandmarkLanguageBased, landmarkObject=landmark, lang=language)
        print(langlandmark)
        serializer = LandmarksSerializer(langlandmark)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandmarkEventCoreListView(APIView):

    def get(self, request, format=None):

        events = LandmarkEvent.objects.all()
        # print(governorates)
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        mainserializer = EventSerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            event = get_object_or_404(
                LandmarkEvent, id=mainserializer.data.get("id"))
            # print(event, "\n\n\n")
            languages = Language.objects.all()

            request.data['eventObject'] = event.id

            eventlangVersions = []
            eventlangVersionsErrors = []
            for language in languages:
                request.data['lang'] = language.id
                # print(request.data, "\n\n")
                serializer = EventsSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    eventlangVersions.append(serializer.data)
                else:
                    eventlangVersionsErrors.append(serializer.errors)

            if len(eventlangVersionsErrors) > 0:
                return Response(eventlangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(eventlangVersions, status=status.HTTP_201_CREATED)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)
