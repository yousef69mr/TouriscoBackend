
from django.http import QueryDict
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from django.contrib.contenttypes.models import ContentType


from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from system.models import Language,Image
from system.serializers import ImageSerializer
from .serializers import (
    ReviewImagesSerializer,
    ReviewSerializer
)
from .models import (
    Review, 
    ReviewImage
)

# Create your views here.

# class TicketsView(APIView):
#     # queryset = LandmarkLanguageBased.objects.all()
#     # serializer_class = LandmarksSerializer
#     lookup_field = 'lang_code'
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request, lang_code, format=None):

#         language = get_object_or_404(Language, code=lang_code)
#         if language is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         tickets = TicketLanguageBased.objects.filter(lang=language)
#         # print(governorates)
#         serializer = TicketsSerializer(tickets, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request,lang_code, format=None):
#         request_data_copy = request.data.copy()
#         language = get_object_or_404(Language,code=lang_code)
#         request_data_copy['lang'] = language.id
#         mainserializer = TicketsSerializer(data=request_data_copy)
#         if mainserializer.is_valid():
#             mainserializer.save()

#             return Response(mainserializer.data, status=status.HTTP_201_CREATED)
#         return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

# # single Ticket
# class TicketView(APIView):
#     # queryset = LandmarkLanguageBased.objects.all()
#     # serializer_class = LandmarksSerializer
#     # lookup_field = ['lang_code', 'landmark_id']
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request, ticket_id, lang_code, format=None):

#         language = get_object_or_404(Language, code=lang_code)
#         ticket = get_object_or_404(Ticket, id=ticket_id)
#         langTicket = get_object_or_404(
#             TicketLanguageBased, ticketObject=ticket, lang=language)
#         print(langTicket)
#         serializer = TicketsSerializer(langTicket)

#         return Response(serializer.data, status=status.HTTP_200_OK)

# get all landmark events core 
# class TicketCoreListView(APIView):

#     def get(self, request, format=None):

#         tickets = Ticket.objects.all()
#         # print(governorates)
#         serializer = TicketSerializer(tickets, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, format=None):
#         # print(request.data)
#         mainserializer = TicketSerializer(data=request.data)

#         if mainserializer.is_valid():
#             mainserializer.save()

#             ticket = get_object_or_404(
#                 Ticket, id=mainserializer.data.get("id"))
#             # print(event, "\n\n\n")
#             try:
#                 languages = Language.objects.all()

#                 request_data_copy = request.data.copy()
#                 request_data_copy['ticketObject'] = ticket.id

#                 ticketlangVersions = []
#                 ticketlangVersionsErrors = []
#                 for language in languages:
#                     request_data_copy['lang'] = language.id
#                     # print(request.data, "\n\n")
#                     serializer = TicketsSerializer(data=request_data_copy)

#                     if serializer.is_valid():
#                         serializer.save()
#                         ticketlangVersions.append(serializer.data)
#                     else:
#                         ticketlangVersionsErrors.append(serializer.errors)

#                 if len(ticketlangVersionsErrors) > 0:
#                     ticket.delete()
#                     return Response(ticketlangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response(ticketlangVersions, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 ticket.delete()
#                 return Response(e, status=status.HTTP_400_BAD_REQUEST)

#         return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class TicketsForSpecificLandmarkEvent(APIView):
#     def get(self, request,lang_code, event_id, format=None):
#         try:
#             language = Language.objects.get(code=lang_code)

#             event = get_object_or_404(LandmarkEvent,id=event_id)
            
#             tickets = TicketLanguageBased.objects.filter(lang=language,ticketObject__eventObject=event)
#             serializer = TicketsSerializer(tickets, many=True)

#             return Response(serializer.data,status=status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReviewListView(APIView):
    def get(self, request, format=None):
        try:
            review_list = Review.objects.all()
            serializer = ReviewSerializer(review_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# single Ticket
class ReviewView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    # lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, review_id, format=None):

        review = get_object_or_404(Review, id=review_id)
        
        serializer = ReviewSerializer(review)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewImagesView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get(self, request, review_id):
        # print(review_id)
        review = get_object_or_404(Review, id=review_id)
        # print(review)
        images = review.images.all()
        # print(images)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, review_id):
        # try:
            review = get_object_or_404(Review,id=review_id)
            
            # print(landmark)
            image_list= request.data.pop('image_list',None)
            request_data_copy = request.data.copy()
            request_data_copy['userObject'] = 1
            # request_data_copy['content_object'] = landmark
            # print("request_data_copy")
            request_data_copy['content_type'] = ContentType.objects.get_for_model(Review).id
            request_data_copy['object_id'] = review.id
            image_response =[]
            error_list = []
            for image in image_list:
                request_data_copy['image']=image
                # print(request_data_copy)
                serializer = ImageSerializer(data=request_data_copy)
                print('here')
                if serializer.is_valid():
                    serializer.save()
                    image = get_object_or_404(Image,id=serializer.data.get('id'))
                    # image.contains_nudity = contains_nudity
                    # print(image)
                    data = QueryDict(mutable=True)
                    data['review'] = review.id
                    data['image'] = image.id
                    
                    reviewImageSerializer = ReviewImagesSerializer(data=data)
                    if reviewImageSerializer.is_valid():
                        reviewImageSerializer.save()
                        image_response.append(serializer.data)
                    # serialized_data = serializer.data
                    else:
                        error_list.append(reviewImageSerializer.errors)
                        image.delete()
                else:
                    error_list.append(serializer.errors)
                    image.delete()
                    
            if len(error_list)>0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:        # serialized_data['contains_nudity'] = contains_nudity
                return Response(image_response, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
