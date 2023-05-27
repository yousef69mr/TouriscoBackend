
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


class LandmarkEventListForSpecificLandmarkView(APIView):
    # lookup_field = ['lang_code', 'landmark_id']

    # get events for specfic landmark
    def get(self, request, lang_code, landmark_id, format=None):

        language = get_object_or_404(Language, code=lang_code)
        landmark = get_object_or_404(Landmark, id=landmark_id)
        # events = LandmarkEvent.objects.filter(
        #     landmarkObject=landmark).only('id').all()
        lang_events = LandmarkEventLanguageBased.objects.filter(lang=language, eventObject__landmarkObject=landmark)
        # print(events)
        serializer = EventsSerializer(lang_events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# single Event
class LandmarkEventView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'event_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, event_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        event = get_object_or_404(LandmarkEvent, id=event_id)
        langevent = get_object_or_404(
            LandmarkEventLanguageBased, eventObject=event, lang=language)
        # print(langevent)
        serializer = EventsSerializer(langevent)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LandmarkEventListView(APIView):
     
    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        # events = LandmarkEvent.objects.filter(
        #     landmarkObject=landmark).only('id').all()
        lang_events = LandmarkEventLanguageBased.objects.filter(lang=language)
        # print(events)
        serializer = EventsSerializer(lang_events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



# get all landmark events core 
class LandmarkEventCoreListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):

        events = LandmarkEvent.objects.all()
        # print(governorates)
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # print(request.data)
        mainserializer = EventSerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            event = get_object_or_404(
                LandmarkEvent, id=mainserializer.data.get("id"))
            # print(event, "\n\n\n")
            try:
                languages = Language.objects.all()
            
                request_data_copy = request.data.copy()
                request_data_copy['eventObject'] = event.id

                eventlangVersions = []
                eventlangVersionsErrors = []
                for language in languages:
                    request_data_copy['lang'] = language.id
                    # print(request.data, "\n\n")
                    serializer = EventsSerializer(data=request_data_copy)

                    if serializer.is_valid():
                        serializer.save()
                        eventlangVersions.append(serializer.data)
                    else:
                        eventlangVersionsErrors.append(serializer.errors)

                if len(eventlangVersionsErrors) > 0:
                    event.delete()
                    return Response(eventlangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(eventlangVersions, status=status.HTTP_201_CREATED)
            except Exception as e:
                    event.delete()
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)
