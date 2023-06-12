
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from landmark_events.models import LandmarkEvent
from system.models import Language

from .serializers import (
    TicketSerializer,
    TicketsSerializer
)
from .models import (
    Ticket, 
    TicketLanguageBased
   
)

# Create your views here.

class TicketsView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        if language is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        tickets = TicketLanguageBased.objects.filter(lang=language)
        # print(governorates)
        serializer = TicketsSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,lang_code, format=None):
        request_data_copy = request.data.copy()
        language = get_object_or_404(Language,code=lang_code)
        request_data_copy['lang'] = language.id
        mainserializer = TicketsSerializer(data=request_data_copy)
        if mainserializer.is_valid():
            mainserializer.save()

            return Response(mainserializer.data, status=status.HTTP_201_CREATED)
        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class LandmarkEventListView(APIView):
#     # lookup_field = ['lang_code', 'landmark_id']

#     # get events for specfic landmark
#     def get(self, request, lang_code, landmark_id, format=None):

#         language = get_object_or_404(Language, code=lang_code)
#         landmark = get_object_or_404(Landmark, id=landmark_id)
#         # events = LandmarkEvent.objects.filter(
#         #     landmarkObject=landmark).only('id').all()
#         lang_events = LandmarkEventLanguageBased.objects.filter(lang=language, eventObject__landmarkObject=landmark)
#         # print(events)
#         serializer = EventsSerializer(lang_events, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

# single Ticket
class TicketView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    # lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, ticket_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        ticket = get_object_or_404(Ticket, id=ticket_id)
        langTicket = get_object_or_404(
            TicketLanguageBased, ticketObject=ticket, lang=language)
        print(langTicket)
        serializer = TicketsSerializer(langTicket)

        return Response(serializer.data, status=status.HTTP_200_OK)

# get all landmark events core 
class TicketCoreListView(APIView):

    def get(self, request, format=None):

        tickets = Ticket.objects.all()
        # print(governorates)
        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # print(request.data)
        mainserializer = TicketSerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            ticket = get_object_or_404(
                Ticket, id=mainserializer.data.get("id"))
            # print(event, "\n\n\n")
            try:
                languages = Language.objects.all()

                request_data_copy = request.data.copy()
                request_data_copy['ticketObject'] = ticket.id

                ticketlangVersions = []
                ticketlangVersionsErrors = []
                for language in languages:
                    request_data_copy['lang'] = language.id
                    # print(request.data, "\n\n")
                    serializer = TicketsSerializer(data=request_data_copy)

                    if serializer.is_valid():
                        serializer.save()
                        ticketlangVersions.append(serializer.data)
                    else:
                        ticketlangVersionsErrors.append(serializer.errors)

                if len(ticketlangVersionsErrors) > 0:
                    ticket.delete()
                    return Response(ticketlangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(ticketlangVersions, status=status.HTTP_201_CREATED)
            except Exception as e:
                ticket.delete()
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TicketsForSpecificLandmarkEvent(APIView):
    def get(self, request,lang_code, event_id, format=None):
        event = get_object_or_404(LandmarkEvent,id=event_id)
        try:
            language = Language.objects.get(code=lang_code)
            
            tickets = TicketLanguageBased.objects.filter(lang=language,ticketObject__eventObject=event)
            serializer = TicketsSerializer(tickets, many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

