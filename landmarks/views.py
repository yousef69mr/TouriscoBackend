
from rest_framework import status
from rest_framework.views import APIView
from django.http import QueryDict

from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,IsAuthenticated)
from system.serializers import ImageSerializer
from system.models import Image
from reviews.serializers import ReviewSerializer,ReviewImagesSerializer
from reviews.models import Review
from categories.models import TourismCategory

from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import (
    LandmarkSerializer,
    LandmarksSerializer,
    LandmarkImagesSerializer,
    LandmarkReviewsSerializer,
    LandmarkTourismCategorySerializer
)
from .models import (
    Language,
    Landmark,
    LandmarkLanguageBased,
)

# Create your views here.
class LandmarkReviewsView(APIView):
    
    permission_classes=[IsAuthenticatedOrReadOnly]


    def get(self, request, landmark_id):
        landmark = get_object_or_404(Landmark, id=landmark_id)
        reviews = landmark.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, landmark_id):
        try:
            landmark = get_object_or_404(Landmark,id=landmark_id)
            
            # print(landmark)
            # image_list= request.data.pop('image_list',None)
            request_data_copy = request.data.copy()
            request_data_copy['userObject'] = request.user.id
            # request_data_copy['content_object'] = landmark
            # print("request_data_copy")
            request_data_copy['content_type'] = ContentType.objects.get_for_model(Landmark).id
            request_data_copy['object_id'] = landmark.id
            review_response =[]
            error_list = []
            
            # print(request_data_copy)
            serializer = ReviewSerializer(data=request_data_copy)
            print('here')
            if serializer.is_valid():
                serializer.save()
                review = get_object_or_404(Review,id=serializer.data.get('id'))
                # image.contains_nudity = contains_nudity
                # print(image)
                data = QueryDict(mutable=True)
                data['landmark'] = landmark.id
                data['review'] = review.id
                print(data)
                landmarkReviewSerializer = LandmarkReviewsSerializer(data=data)
                if landmarkReviewSerializer.is_valid():
                    landmarkReviewSerializer.save()
                    review_response.append(serializer.data)
                # serialized_data = serializer.data
                else:
                    error_list.append(landmarkReviewSerializer.errors)
                    review.delete()
            else:
                error_list.append(serializer.errors)
                
                    
            if len(error_list)>0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:        # serialized_data['contains_nudity'] = contains_nudity
                return Response(review_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LandmarkImagesView(APIView):
    
    permission_classes=[IsAuthenticatedOrReadOnly]


    def get(self, request, landmark_id):
        landmark = get_object_or_404(Landmark, id=landmark_id)
        images = landmark.images.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, landmark_id):
        landmark = get_object_or_404(Landmark,id=landmark_id)
        try:
            # print(landmark)
            image_list= request.data.pop('image_list',None)
            request_data_copy = request.data.copy()
            request_data_copy['userObject'] = request.user.id
            # request_data_copy['content_object'] = landmark
            # print("request_data_copy")
            request_data_copy['content_type'] = ContentType.objects.get_for_model(Landmark).id
            request_data_copy['object_id'] = landmark.id
            image_response =[]
            error_list = []
            for image in image_list:
                request_data_copy['image']=image
                # print(request_data_copy)
                serializer = ImageSerializer(data=request_data_copy)
                # print('here')
                if serializer.is_valid():
                    serializer.save()
                    image = get_object_or_404(Image,id=serializer.data.get('id'))
                    # image.contains_nudity = contains_nudity
                    # print(image)
                    data = QueryDict(mutable=True)
                    data['landmark'] = landmark.id
                    data['image'] = image.id
                    
                    landmarkImageSerializer = LandmarkImagesSerializer(data=data)
                    if landmarkImageSerializer.is_valid():
                        landmarkImageSerializer.save()
                        image_response.append(serializer.data)
                    # serialized_data = serializer.data
                    else:
                        error_list.append(landmarkImageSerializer.errors)
                        image.delete()
                else:
                    error_list.append(serializer.errors)
                    image.delete()
                    
            if len(error_list)>0:
                return Response(error_list, status=status.HTTP_400_BAD_REQUEST)
            else:        # serialized_data['contains_nudity'] = contains_nudity
                return Response(image_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LandmarkListView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        try:
                
            landmarks = LandmarkLanguageBased.objects.filter(lang=language).order_by('-landmarkObject__num_of_views')
            # print(governorates)
            serializer = LandmarksSerializer(landmarks, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class LandmarkInSpecificGovernorateView(APIView):
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, governorate_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        # governorate = get_object_or_404(Governorate, id=governorate_id)
        # print(governorate)
        langlandmarks = LandmarkLanguageBased.objects.filter(landmarkObject__govObject__id=governorate_id, lang=language)
        print(langlandmarks)
        serializer = LandmarksSerializer(langlandmarks,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LandmarkWithSpecificTourismCategoryView(APIView):
    # lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, tourism_category_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        # governorate = get_object_or_404(Governorate, id=governorate_id)
        # print(governorate)
        langlandmarks = LandmarkLanguageBased.objects.filter(landmarkObject__tourismCategoryObject__id=tourism_category_id, lang=language)
        print(langlandmarks)
        serializer = LandmarksSerializer(langlandmarks,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LandmarkWithSpecificTypeCategoryView(APIView):
    # lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, type_category_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        # governorate = get_object_or_404(Governorate, id=governorate_id)
        # print(governorate)
        langlandmarks = LandmarkLanguageBased.objects.filter(landmarkObject__typeCategoryObject__id=type_category_id, lang=language)
        print(langlandmarks)
        serializer = LandmarksSerializer(langlandmarks,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class IncreaseLandmarkViewsView(APIView):
    def post(self, request, landmark_id, format=None):
        landmark = get_object_or_404(Landmark, id=landmark_id)
        print(landmark)
        try:
            landmark.increase_views()
            landmark.save()
            return Response({'message':"increased successfully"},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)




class LandmarkView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, landmark_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        landmark = get_object_or_404(Landmark, id=landmark_id)
        print(landmark)
        landmark.increase_views()
        landmark.save()
        langlandmark = get_object_or_404(LandmarkLanguageBased, landmarkObject=landmark, lang=language)
        print(langlandmark)
        serializer = LandmarksSerializer(langlandmark)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, landmark_id, format=None):
        landmark = get_object_or_404(Landmark, id=landmark_id)
        try:
            serializer = LandmarkSerializer(landmark, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, landmark_id, format=None):
        landmark = get_object_or_404(Landmark, id=landmark_id)
        landmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
class LandmarkCoreListView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):

        landmarks = Landmark.objects.all()
        # print(governorates)
        serializer = LandmarkSerializer(landmarks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        try:
            copy_data = request.data.copy()
            copy_data['user_created_by'] =  request.user.id
            mainserializer = LandmarkSerializer(data=copy_data)

            if mainserializer.is_valid():
                mainserializer.save()

                landmark = Landmark.objects.get(id=mainserializer.data.get("id"))

                languages = Language.objects.all()
                request_data_copy = request.data.copy()
                request_data_copy.pop('image', None)
                
                # request_data_copy['tourism_categories'] = 1,2,3
                tourism_categories_list = request_data_copy.get('tourism_categories',[])

                if len(tourism_categories_list) == 0:
                    tourismCategoryObject = request_data_copy.get('tourismCategoryObject',None)
                    if tourismCategoryObject is not None:
                        tourism_categories_list.append(tourismCategoryObject)

                if len(tourism_categories_list) > 0:
                    # print(len(tourism_categories_list))
                    # print(tourism_categories_list)
                    # Add the categories to the landmark object
                    for category_id in tourism_categories_list:
                        try:
                            category = TourismCategory.objects.get(id=category_id)
                        except:
                            category = None

                        if category is not None :
                            data = QueryDict(mutable=True)
                            data['landmarkObject'] = landmark.id
                            data['categoryObject'] = category.id

                            tourism_categories_serializer = LandmarkTourismCategorySerializer(data=data)
                            if tourism_categories_serializer.is_valid():
                                tourism_categories_serializer.save()
                            
                

                request_data_copy['landmarkObject'] = landmark.id

                landmarklangVersions = []
                landmarklangVersionsErrors = []

                for language in languages:
                    request_data_copy['lang'] = language.id
                    serializer = LandmarksSerializer(data=request_data_copy)

                    if serializer.is_valid():
                        serializer.save()
                        landmarklangVersions.append(serializer.data)
                    else:
                        landmarklangVersionsErrors.append(serializer.errors)

                if len(landmarklangVersionsErrors) > 0:
                    landmark.delete()
                    return Response(landmarklangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(landmarklangVersions, status=status.HTTP_201_CREATED)
            else:
                return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as e:
            return Response({"error":f"KeyError {e}"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            del mainserializer
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    

class UserLandmarkListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,lang_code):
        language = get_object_or_404(Language,code=lang_code)
        try:
            landmarks = LandmarkLanguageBased.objects.filter(landmarkObject__user_created_by=request.user.id,lang=language)
            serializer = LandmarksSerializer(landmarks,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class LandmarkReviewsWithImagesView(APIView):
    
    permission_classes=[IsAuthenticatedOrReadOnly]


    def get(self, request, landmark_id):
        landmark = get_object_or_404(Landmark, id=landmark_id)
        reviews = landmark.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, landmark_id):
        try:
            landmark = get_object_or_404(Landmark,id=landmark_id)
            
            request_data_copy = request.data.copy()
            request_data_copy['userObject'] = request.user.id
           
            request_data_copy['content_type'] = ContentType.objects.get_for_model(Landmark).id
            request_data_copy['object_id'] = landmark.id
            
            error_list = []
            
            # print(request_data_copy)
            serializer = ReviewSerializer(data=request_data_copy)
            # print('here')
            if serializer.is_valid():
                serializer.save()
                review = get_object_or_404(Review,id=serializer.data.get('id'))
                # image.contains_nudity = contains_nudity
                # print(image)
                data = QueryDict(mutable=True)
                data['landmark'] = landmark.id
                data['review'] = review.id
                # print(data)
                landmarkReviewSerializer = LandmarkReviewsSerializer(data=data)
                if landmarkReviewSerializer.is_valid():
                    landmarkReviewSerializer.save()

                    # checking image 
                    image_list = request_data_copy.pop('image_list',[])
                    image_response = []
                    if len(image_list) > 0:
                        for image in image_list:
                            request_data_copy['image'] = image
                            # print(request_data_copy)
                            image_serializer = ImageSerializer(data=request_data_copy)
                            # print('here')
                            if image_serializer.is_valid():
                                image_serializer.save()
                                image = get_object_or_404(Image,id=image_serializer.data.get('id'))
                                # image.contains_nudity = contains_nudity
                                # print(image)
                                # print('here')
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
                                error_list.append(image_serializer.errors)
                            


                    # review_response.append(serializer.data)

                    review_serializer = ReviewSerializer(review)

                       
            if len(error_list)>0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:        # serialized_data['contains_nudity'] = contains_nudity
                return Response(review_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
