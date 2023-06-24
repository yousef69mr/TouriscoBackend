
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
        try:
            # print(landmark)
            image_list= request.data.pop('image_list',None)
            request_data_copy = request.data.copy()
            request_data_copy['userObject'] = request.user.id
            # print(request.user.id)
            # print(request_data_copy)
            # request_data_copy['content_object'] = landmark
            # print("request_data_copy")
            request_data_copy['content_type'] = ContentType.objects.get_for_model(Review).id
            request_data_copy['object_id'] = review.id
            image_response = []
            error_list = []
            for image in image_list:
                request_data_copy['image'] = image
                # print(request_data_copy)
                serializer = ImageSerializer(data=request_data_copy)
                print('here')
                if serializer.is_valid():
                    serializer.save()
                    image = get_object_or_404(Image,id=serializer.data.get('id'))
                    # image.contains_nudity = contains_nudity
                    # print(image)
                    print('here')
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
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
