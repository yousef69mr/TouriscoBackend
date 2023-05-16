
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)

import copy

from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import (
    LandmarkSerializer,
    LandmarksSerializer,
   
)
from .models import (
    Language,
    Landmark,
    LandmarkLanguageBased,
)

# Create your views here.



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

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandmarkInSpecificGovernorate(APIView):
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

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        mainserializer = LandmarkSerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()
            print('\n\n\ni\n\n\n')

            landmark = get_object_or_404(
                Landmark, id=mainserializer.data.get("id"))
            # print(landmark)
            # landmark = get_object_or_404(
            #     Landmark, id=17)

            # print(event, "\n\n\n")
            try:
                languages = Language.objects.all()
                # request_data_copy.pop('image')
                request.data.pop('image')
                request_data_copy = request.data.copy()
                # print(request_data_copy)
                # request_data_copy['image']=request.data['image']
                request_data_copy['landmarkObject'] = landmark.id
                # print(request_data_copy)
                landmarklangVersions = []
                landmarklangVersionsErrors = []
                for language in languages:
                    request_data_copy['lang'] = language.id
                    # print(request.data, "\n\n")
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
            except Exception as e:
                landmark.delete()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, format=None):
    #     mainserializer = LandmarkSerializer(data=request.data)

    #     if mainserializer.is_valid():
    #         mainserializer.save()

    #         landmark = get_object_or_404(
    #             Landmark, id=mainserializer.data.get("id"))
    #         # landmark = get_object_or_404(
    #         #     Landmark, id=17)

    #         print(landmark, "\n\n\n")
    #         # request.data.pop('image', None)
    #         try:
    #             languages = Language.objects.all()
                
    #             request_data_copy = request.data.copy()
    #             request_data_copy.pop('image')
    #             # print(request_data_copy)
    #             # request_data_copy['image']=request.data['image']
    #             request_data_copy['landmarkObject'] = landmark.id
    #             # print(request_data_copy)
    #             landmarklangVersions = []
    #             landmarklangVersionsErrors = []
    #             for language in languages:
    #                 request_data_copy['lang'] = language.id
    #                 print(request.data, "\n\n")
    #                 serializer = LandmarksSerializer(data=request_data_copy)

    #                 if serializer.is_valid():
    #                     serializer.save()
    #                     landmarklangVersions.append(serializer.data)
    #                 else:
    #                     landmarklangVersionsErrors.append(serializer.errors)

    #             if len(landmarklangVersionsErrors) > 0:
    #                 landmark.delete()
    #                 return Response(landmarklangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 return Response(landmarklangVersions, status=status.HTTP_201_CREATED)
    #         except Exception as e:
    #             landmark.delete()
    #             return Response(e, status=status.HTTP_400_BAD_REQUEST)

    #     return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)

