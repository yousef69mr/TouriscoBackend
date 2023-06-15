from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,IsAdminUser)
from django.shortcuts import get_object_or_404
# from landmarks.models import LandmarkLanguageBased
from system.models import Language
# from landmarks.serializers import LandmarksSerializer
from .models import (
    TourismCategory,
    TourismCategoryLanguageBased,
    TypeCategory,
    TypeCategoryLanguageBased,
    TicketClassCategory,
    TicketClassCategoryLanguageBased
)
from .serializers import (
    TourismCategoriesSerializer,
    TourismCategorySerializer,
    TypeCategoriesSerializer,
    TypeCategorySerializer,
    TicketClassCategoriesSerializer,
    TicketClassCategorySerializer
)

# Create your views here.

class  TourismCategoriesListView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)

        categories = TourismCategoryLanguageBased.objects.all().filter(lang=language)
        # print(governorates)
        serializer = TourismCategoriesSerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TourismCategoryView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, category_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        category = get_object_or_404(TourismCategory, id=category_id)
        print(category)
        langcategory = get_object_or_404(
            TourismCategoryLanguageBased, categoryObject=category, lang=language)
        print(langcategory)
        serializer = TourismCategoriesSerializer(langcategory)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TourismCategoriesCoreListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):

        categories = TourismCategory.objects.all()
        # print(governorates)
        serializer = TourismCategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        mainserializer = TourismCategorySerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            category = get_object_or_404(
                TourismCategory, id=mainserializer.data.get("id"))
            # category =  get_object_or_404(
            #     TourismCategory, id=7)

            # print(category, "\n\n\n")
            try:
                languages = Language.objects.all()

                request_data_copy = request.data.copy()

                request_data_copy['categoryObject'] = category.id
                # print(request_data_copy)
                categorylangVersions = []
                categorylangVersionsErrors = []
                for language in languages:
                    request_data_copy['lang'] = language.id
                    # print(request.data, "\n\n")
                    serializer = TourismCategoriesSerializer(data=request_data_copy)

                    if serializer.is_valid():
                        serializer.save()
                        categorylangVersions.append(serializer.data)
                    else:
                        categorylangVersionsErrors.append(serializer.errors)

                if len(categorylangVersionsErrors) > 0:
                    category.delete()
                    return Response(categorylangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(categorylangVersions, status=status.HTTP_201_CREATED)
            except Exception as e:
                category.delete()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)


class  TypeCategoriesListView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)

        categories = TypeCategoryLanguageBased.objects.all().filter(lang=language)
        # print(governorates)
        serializer = TypeCategoriesSerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TypeCategoryView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, category_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        category = get_object_or_404(TypeCategory, id=category_id)
        print(category)
        langcategory = get_object_or_404(TourismCategoryLanguageBased, categoryObject=category, lang=language)
        print(langcategory)
        serializer = TypeCategoriesSerializer(langcategory)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TypeCategoriesCoreListView(APIView):

    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):

        categories = TypeCategory.objects.all()
        # print(governorates)
        serializer = TypeCategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        mainserializer = TypeCategorySerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            category = get_object_or_404(TypeCategory, id=mainserializer.data.get("id"))
            # category =  get_object_or_404(
            #     TourismCategory, id=7)

            # print(category, "\n\n\n")
            try:
                languages = Language.objects.all()

                request_data_copy = request.data.copy()

                request_data_copy['categoryObject'] = category.id
                # print(request_data_copy)
                categorylangVersions = []
                categorylangVersionsErrors = []
                for language in languages:
                    request_data_copy['lang'] = language.id
                    # print(request.data, "\n\n")
                    serializer = TypeCategoriesSerializer(data=request_data_copy)

                    if serializer.is_valid():
                        serializer.save()
                        categorylangVersions.append(serializer.data)
                    else:
                        categorylangVersionsErrors.append(serializer.errors)

                if len(categorylangVersionsErrors) > 0:
                    category.delete()
                    return Response(categorylangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(categorylangVersions, status=status.HTTP_201_CREATED)
            except Exception as e:
                category.delete()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)



class  TicketClassCategoriesListView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = 'lang_code'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)

        categories = TicketClassCategoryLanguageBased.objects.all().filter(lang=language)
        # print(governorates)
        serializer = TicketClassCategoriesSerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketClassCategoryView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, ticket_class_category_id, lang_code, format=None):

        language = get_object_or_404(Language, code=lang_code)
        category = get_object_or_404(TicketClassCategory, id=ticket_class_category_id)
        print(category)
        langcategory = get_object_or_404(TicketClassCategoryLanguageBased, categoryObject=category, lang=language)
        print(langcategory)
        serializer = TicketClassCategoriesSerializer(langcategory)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketClassCategoriesCoreListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):

        categories = TicketClassCategory.objects.all()
        # print(governorates)
        serializer = TicketClassCategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        mainserializer = TicketClassCategorySerializer(data=request.data)

        if mainserializer.is_valid():
            mainserializer.save()

            category = get_object_or_404(TicketClassCategory, id=mainserializer.data.get("id"))
            # category =  get_object_or_404(
            #     TourismCategory, id=7)

            # print(category, "\n\n\n")
            try:
                languages = Language.objects.all()

                request_data_copy = request.data.copy()

                request_data_copy['categoryObject'] = category.id
                # print(request_data_copy)
                categorylangVersions = []
                categorylangVersionsErrors = []
                for language in languages:
                    request_data_copy['lang'] = language.id
                    # print(request.data, "\n\n")
                    serializer = TicketClassCategoriesSerializer(data=request_data_copy)

                    if serializer.is_valid():
                        serializer.save()
                        categorylangVersions.append(serializer.data)
                    else:
                        categorylangVersionsErrors.append(serializer.errors)

                if len(categorylangVersionsErrors) > 0:
                    category.delete()
                    return Response(categorylangVersionsErrors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(categorylangVersions, status=status.HTTP_201_CREATED)
            except Exception as e:
                category.delete()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(mainserializer.errors, status=status.HTTP_400_BAD_REQUEST)
