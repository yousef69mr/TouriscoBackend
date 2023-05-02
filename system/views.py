
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import (
    GovernoratesSerializer,
    GovernorateSerializer,
    LanguageSerializer,
    LandmarkSerializer,
    LandmarksSerializer,
    TicketsSerializer,
    EventSerializer,
    EventsSerializer,
    LanguageSerializer
)
from .models import (
    Language,
    Governorate,
    GovernorateLanguageBased,
    Landmark,
    LandmarkLanguageBased,
    TicketLanguageBased,
    LandmarkEvent,
    LandmarkEventLanguageBased
)

# Create your views here.


class LanguageView(viewsets.ModelViewSet):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]


class GovernorateListView(APIView):
    # queryset = GovernorateLanguageBased.objects.all()
    # serializer_class = GovernoratesSerializer
    lookup_field = 'lang_code'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)

        governorates = GovernorateLanguageBased.objects.all().filter(lang=language)
        # print(governorates)
        serializer = GovernoratesSerializer(governorates, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = GovernoratesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GovernorateCoreListView(APIView):
    def get(self, request, format=None):

        governorates = get_list_or_404(Governorate)
        # print(governorates)
        serializer = GovernorateSerializer(governorates, many=True)

        return Response({"governorates": serializer.data}, status=status.HTTP_200_OK)


class GovernorateView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, governorate_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        governorate = get_object_or_404(Governorate, id=governorate_id)
        langGovernorate = get_object_or_404(
            GovernorateLanguageBased, govObject=governorate, lang=language)
        print(langGovernorate)
        serializer = GovernoratesSerializer(langGovernorate)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandmarkListView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)

        landmarks = LandmarkLanguageBased.objects.all().filter(lang=language)
        # print(governorates)
        serializer = LandmarksSerializer(landmarks, many=True)

        return Response({"landmarks": serializer.data}, status=status.HTTP_200_OK)


class LandmarkView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, landmark_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        landmark = get_object_or_404(Landmark, id=landmark_id)
        print(landmark)
        langlandmark = get_object_or_404(
            LandmarkLanguageBased, landmarkObject=landmark, lang=language)
        print(langlandmark)
        serializer = LandmarksSerializer(langlandmark)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandmarkCoreListView(APIView):
    def get(self, request, format=None):

        landmarks = Landmark.objects.all()
        # print(governorates)
        serializer = LandmarkSerializer(landmarks, many=True)

        return Response({"landmarks": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        mainserializer = LandmarkSerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            landmark = get_object_or_404(
                Landmark, id=mainserializer.data.get("id"))

            # print(event, "\n\n\n")
            languages = Language.objects.all()

            request.data['landmarkObject'] = landmark.id

            landmarklangVersions = []
            landmarklangVersionsErrors = []
            for language in languages:
                request.data['lang'] = language.id
                # print(request.data, "\n\n")
                serializer = LandmarksSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    landmarklangVersions.append(serializer.data)
                else:
                    landmarklangVersionsErrors.append(serializer.errors)

            if len(landmarklangVersionsErrors) > 0:
                return Response({f'landmark #{landmark.id}': landmarklangVersionsErrors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({f'landmark #{landmark.id}': landmarklangVersions}, status=status.HTTP_201_CREATED)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        return Response({f"Landmark #{landmark.id} events": serializer.data}, status=status.HTTP_200_OK)


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

        return Response({"Landmark events": serializer.data}, status=status.HTTP_200_OK)

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
                return Response({f'event #{event.id}': eventlangVersionsErrors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({f'event #{event.id}': eventlangVersions}, status=status.HTTP_201_CREATED)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketsView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        if language is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tickets = TicketLanguageBased.objects.all().filter(lang=language)
        # print(governorates)
        serializer = TicketsSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        mainserializer = TicketsSerializer(data=request.data)
        if mainserializer.is_valid():
            mainserializer.save()

            return Response(mainserializer.data, status=status.HTTP_201_CREATED)
        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)
