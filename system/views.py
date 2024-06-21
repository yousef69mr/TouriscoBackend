
from rest_framework import viewsets, status
from rest_framework.views import APIView
# from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from TouriscoBackend.utils import isInteger

# import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import GoogleAPIError
import dialogflow

import os
from TouriscoBackend.settings import BASE_DIR

from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from landmarks.models import LandmarkLanguageBased,Landmark,LandmarkTourismCategory
from categories.models import TourismCategoryLanguageBased,TourismCategory
from tour_packages.models import TourPackage

from .serializers import (
    ImageSerializer,
    LanguageSerializer,
)
from .models import (
    Language,
    Image
)

# Create your views here.


class LanguageView(viewsets.ModelViewSet):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]


class ImageListView(APIView):
    # authentication_classes = [JWTAuthentication]
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self,request,format=None):
        try:
            # user = request.user
            images = Image.objects.all()
            serializer = ImageSerializer(images,many=True)
            # print(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class ImageView(APIView):
    # authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request,image_id,format=None):
        image = get_object_or_404(Image,id=image_id)
        try:
            # user = request.user
            serializer = ImageSerializer(image)
            # print(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
       
def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)

    return data        
class ChatbotView(APIView):

    @csrf_exempt
    def post(self, request):
        agent_language_code = 'en'
        from googletrans import Translator
        translator=Translator()
        print(request.data)
        desired_language=request.data.get('language_code','ar')
        input_text = request.data.get('message','')
        # print(input_text)
        input_text = translator.translate(text=str(input_text),dest=agent_language_code).text
        print(input_text)
        try:
            
            GOOGLE_AUTHENTICATION_FILE_NAME = "tourisco-494f889ff6ac.json"
            current_directory = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
            # print(path)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

            GOOGLE_PROJECT_ID = "tourisco"
            session_id = request.POST.get('session_id','1234567891')
            context_short_name = "does_not_matter"

            context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + \
                    context_short_name.lower()

            parameters = dialogflow.types.struct_pb2.Struct()
            #parameters["foo"] = "bar"

            context_1 = dialogflow.types.context_pb2.Context(
                name=context_name,
                lifespan_count=2,
                parameters=parameters
            )
            query_params_1 = {"contexts": [context_1]}
            
            response = detect_intent_with_parameters(
                project_id=GOOGLE_PROJECT_ID,
                session_id=session_id,
                query_params=query_params_1,
                language_code=agent_language_code,
                user_input=input_text
            )
            if agent_language_code  is not desired_language:
                response_text = translator.translate(text=response.query_result.fulfillment_text,src=agent_language_code,dest=desired_language).text
            else:
                response_text = response.query_result.fulfillment_text

            return Response({'response':response_text}, status=status.HTTP_200_OK)
        except GoogleAPIError as e:
            # Handle API errors
            if e.code == 403:
                return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
            elif e.code == 429:
                return Response({'error': 'API rate limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            else:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):
    import random
    defination_responses = ["{title} is {defination}","Defination of {title} is {defination}"]
    recommendation_responses = ["you should visit {places}","you should visit {places} {type}","{places} should be in your next {type}"]
    fallback_responses = ["Sorry, I couldn't find any {details} for {subject}."]
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=user_input, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    #  # Construct the DetectIntentRequest object
    # request = dialogflow.types.DetectIntentRequest(
    #     session=session,
    #     query_input=query_input,
    #     query_params=query_params
    # )

    # Send the request to Dialogflow
    response = session_client.detect_intent(
        session=session,
        query_input=query_input,
        query_params=query_params
    )

    # Extract intent and entities from the response
    query_result = response.query_result
    intent = query_result.intent.display_name
    parameters = query_result.parameters
    


    # # Process entities based on intent
    # if intent == 'recommend_landmarks':
    #     if 'governorate' in parameters.fields:
    #         city = parameters.fields['city'].string_value
    #         landmarks = LandmarkLanguageBased.objects.filter(location=city)
    #         if landmarks.exists():
    #             landmark_names = [l.name for l in landmarks]
    #             parameters.fields['city'].ClearField('string_value')
    #             parameters.fields['landmarks'].ClearField('string_value')
    #             parameters.fields['landmarks'].string_value.extend(landmark_names)
    #         else:
    #             response_text = f"Sorry, I couldn't find any landmarks for {city}."
    #             query_result.fulfillment_text = response_text
    #             return response

    # if intent == 'define_tourism_category':
    #     # print('parameters',parameters.fields)
    #     if 'tourism-category-title' in parameters.fields:
    #         category_title = parameters.fields['tourism-category-title'].string_value
    #         category_obj = TourismCategory.objects.filter(name=category_title.title().replace(" ", "_")).first()
    #         if category_obj:
    #             tourism_category = TourismCategoryLanguageBased.objects.filter(lang__code=language_code, categoryObject=category_obj).first()
    #             if tourism_category:
    #                 parameters.fields['tourism-category-description'].ClearField('string_value')
    #                 # print('parameters',parameters.fields)
    #                 parameters.fields['tourism-category-description'].string_value = tourism_category.description
    #                 # print('parameters',parameters.fields)
                    
    #                 response_text = random.choice(defination_responses).format(title=tourism_category.title,defination=tourism_category.description)
    #                 query_result.fulfillment_text = response_text
    #                 return response
    #             else:
    #                 response_text = random.choice(fallback_responses).format(details="details",subject=tourism_category.title)
    #                 query_result.fulfillment_text = response_text
    #                 return response
    if intent == 'define_objects':
        # print('parameters',parameters.fields)
        object_title = parameters.fields['object_title'].string_value
        print("text",object_title)
        if object_title:
            # category_title = parameters.fields['tourism-category-title'].string_value
            category_obj = TourismCategory.objects.filter(name=object_title.title().replace(" ", "_")).first()
            if category_obj:
                tourism_category = TourismCategoryLanguageBased.objects.filter(lang__code=language_code, categoryObject=category_obj).first()
                if tourism_category:
                    # parameters.fields['tourism-category-description'].ClearField('string_value')
                    # # print('parameters',parameters.fields)
                    # parameters.fields['tourism-category-description'].string_value = tourism_category.description
                    # print('parameters',parameters.fields)
                    
                    response_text = random.choice(defination_responses).format(title=tourism_category.title,defination=tourism_category.description)
                    query_result.fulfillment_text = response_text
                    return response
                else:
                    response_text = random.choice(fallback_responses).format(details="details",subject=tourism_category.title)
                    query_result.fulfillment_text = response_text
                    return response
            else:

                print(object_title.title().replace(" ", "_"))
                landmark_obj = Landmark.objects.filter(name=object_title.title().replace(" ", "_")).first()
                print(landmark_obj)
                if landmark_obj:
                    landmark = LandmarkLanguageBased.objects.filter(lang__code=language_code, landmarkObject=landmark_obj).first()
                    if landmark:
                        # parameters.fields['tourism-category-description'].ClearField('string_value')
                        # # print('parameters',parameters.fields)
                        # parameters.fields['tourism-category-description'].string_value = landmark.description
                        # print('parameters',parameters.fields)
                        
                        response_text = random.choice(defination_responses).format(title=landmark.title,defination=landmark.description)
                        query_result.fulfillment_text = response_text
                        return response
                    else:
                        response_text = random.choice(fallback_responses).format(details="details",subject=object_title)
                        query_result.fulfillment_text = response_text
                        return response
                
    elif intent == 'recommend_objects':
        print('parameters',parameters.fields)
        object_type = parameters.fields['object-type'].string_value
        print(object_type)
        objects=None
        # check number of objects to return
        
        if 'number' in parameters.fields and isInteger(parameters.fields['number'].number_value):
            landmark_number = int(parameters.fields['number'].number_value)
            if landmark_number==0:
                landmark_number = 3
            print(landmark_number)
        else:
            landmark_number = 1
        # elif int(location_type[0]):
        #     landmark_number = int(location_type[0])
         
        
        if 'tourism-category-title' in parameters.fields and len(parameters.fields['tourism-category-title'].list_value)>0:
            category_title_list = parameters.fields['tourism-category-title'].list_value
            
            # print(category_title_list)
            category_titles = [category.title().replace(" ","_") for category in category_title_list]
            # print(category_titles)
            categories =TourismCategory.objects.filter(name__in=category_titles)
            print(categories)
            # landmark_obj = Landmark.objects.filter(name_icontains=landmark_name.title().replace(" ", "_")).first()
            
            
            if object_type == 'landmark':

                objects = LandmarkLanguageBased.objects.filter(lang__code=language_code,landmarkObject__tourism_categories__in=categories).order_by('-landmarkObject__num_of_views')[:landmark_number]
            elif object_type == 'package':
                objects = TourPackage.objects.filter(tourism_categories__in=categories).order_by('-num_of_views')[:landmark_number]
            print(objects)
            print(landmark_number)
            
        else:
            if object_type == 'landmark':

                objects = LandmarkLanguageBased.objects.filter(lang__code=language_code).order_by('-landmarkObject__num_of_views')[:landmark_number]
            elif object_type == 'package':
                objects = TourPackage.objects.all().order_by('-num_of_views')[:landmark_number]
            print(objects)
            print(landmark_number)
        

        # return result
        if objects:
            if isinstance(objects.first(), TourPackage):
                object_names = ', '.join([str(object.title+'_'+str(object.id)) for object in objects])
            else:
                object_names = ', '.join([object.title for object in objects])
            
            print(object_names)
            if isinstance(objects.first(), TourPackage):
                if len(objects)>0:
                    objects_type = 'packages'
                else:
                    objects_type = 'package'

            if isinstance(objects.first(), LandmarkLanguageBased):
                if len(objects)>0:
                    objects_type = 'landmarks'
                else:
                    objects_type = 'landmark'
            else:
                if len(objects)>0:
                    objects_type = 'destinations'
                else:
                    objects_type = 'destination'

            response_text = random.choice(recommendation_responses).format(places=object_names,type=objects_type)
            query_result.fulfillment_text = response_text
            return response
        else:
            response_text = random.choice(fallback_responses).format(details=object_type,subject=category_title_list)
            query_result.fulfillment_text = response_text
            return response

                # landmark = LandmarkLanguageBased.objects.filter(lang__code=language_code, landmarkObject=landmark_obj).first()
                # if landmark:
                #     # parameters.fields['tourism-category-description'].ClearField('string_value')
                #     # # print('parameters',parameters.fields)
                #     # parameters.fields['tourism-category-description'].string_value = landmark.description
                #     # print('parameters',parameters.fields)
                    
                #     response_text = random.choice(defination_responses).format(title=landmark.title,defination=landmark.description)
                #     query_result.fulfillment_text = response_text
                #     return response
                # else:
                #     response_text = f"Sorry, I couldn't find any details for {landmark_name}."
                #     query_result.fulfillment_text = response_text
                #     return response



    # Send the updated parameters back to Dialogflow
    # Create a new QueryParameters object with the updated parameters
    # print('parameters',parameters.fields)
    # print(response)
    # Create a new detect_intent_request message with the updated parameters
    # Create a new DetectIntentRequest message with the updated parameters
    # detect_intent_request = dialogflow.types.DetectIntentRequest(
    #     session=session,
    #     query_input=query_input,
    #     query_params=dialogflow.types.QueryParameters(
    #         contexts=query_result.output_contexts
    #     ),
    #     input=dialogflow.types.QueryInput(
    #         text=text_input,
    #         parameters=parameters
    #     )
    # )

    # # Send the updated parameters back to Dialogflow
    # response = session_client.detect_intent(
    #     request=detect_intent_request
    # )

    # query_params = {"contexts": query_result.output_contexts}
    # query_input = dialogflow.types.QueryInput(text=text_input)
    # response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params)
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    return response



# def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):
#     session_client = dialogflow.SessionsClient()
#     session = session_client.session_path(project_id, session_id)
#     text_input = dialogflow.types.TextInput(text=user_input, language_code=language_code)
#     query_input = dialogflow.types.QueryInput(text=text_input)

#     # Extract intent and entities from user input
#     response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params)
#     query_result = response.query_result
#     intent = query_result.intent.display_name
#     parameters = query_result.parameters

#     # Process entities based on intent
#     if intent == 'recommend_landmarks':
#         if 'governorate' in parameters.fields:
#             city = parameters.fields['city'].string_value
#             landmarks = LandmarkLanguageBased.objects.filter(location=city)
#             landmark_names = [l.name for l in landmarks]
#             parameters.fields['city'].ClearField('string_value')
#             parameters.fields['landmarks'].ClearField('string_value')
#             parameters.fields['landmarks'].string_value.extend(landmark_names)
#     elif intent == 'define_tourism_category':
#         print('parameters',parameters.fields)
#         if 'tourism-category-title' in parameters.fields:
#             category_title = parameters.fields['tourism-category-title'].string_value
#             category_obj = TourismCategory.objects.filter(name=category_title.title().replace(" ", "_")).first()
#             if category_obj:
#                 tourism_category = TourismCategoryLanguageBased.objects.filter(lang__code=language_code, categoryObject=category_obj).first()
#                 if tourism_category:
#                     parameters.fields['tourism-category-description'].ClearField('string_value')
#                     print('parameters',parameters.fields)
#                     parameters.fields['tourism-category-description'].string_value = tourism_category.description
#                     print('parameters',parameters.fields)
#                 else:
#                     response_text = f"Sorry, I couldn't find any tourism category for {category_title}."
#                     query_result.fulfillment_text = response_text
#                     return response
#         # if 'tourism-category-description' in parameters.fields:
#         #     # category_desc = parameters.fields['tourism-category-description'].string_value
#         #     category_title = parameters.fields['tourism-category-title'].string_value
#         #     print(category_title.title().replace(" ", "_"))
#         #     tourism_category = TourismCategoryLanguageBased.objects.filter(lang__code=language_code,categoryObject__name=category_title.title().replace(" ", "_")).first()
#         #     print(tourism_category)
#         #     if tourism_category:
#         #         print(tourism_category.description)
#         #         parameters.fields['tourism-category-description'].ClearField('string_value')
#         #         parameters.fields['tourism-category-description'].string_value = tourism_category.description
#         #     else:
#         #         response_text = f"Sorry, I couldn't find any tourism category for {category_title}."
#         #         query_result.fulfillment_text = response_text
#         #         return response

#     # elif intent == 'request_weather':
#     #     if 'city' in parameters.fields:
#     #         city = parameters.fields['city'].string_value
#     #         weather = get_weather(city)
#     #         parameters.fields['city'].ClearField('string_value')
#     #         parameters.fields['temperature'].number_value = weather['temperature']
#     #         parameters.fields['condition'].string_value = weather['condition']

#     # Send updated parameters to Dialogflow
#     query_params = {"contexts": query_result.output_contexts}
#     query_input = dialogflow.types.QueryInput(text=text_input, parameters=parameters)
#     response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params)

#     return response

from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def dialogflow_webhook(request):
    req = json.loads(request.body)
    print(req)
    intent = req['queryResult']['intent']['displayName']
    if intent == 'Recommend Landmark':
        # Get the landmark type and location from the entities
        landmark_type = req['queryResult']['parameters']['LandmarkType']
        location = req['queryResult']['parameters']['Location']
        # Use the landmark type and location to retrieve data from your Django objects
        # ...
        # response_text = "I recommend visiting {} in {}".format(landmark_name, location)
    elif intent == 'define_tourism_category':
        # Get the landmark type and location from the entities
        category_type = req['queryResult']['parameters']['LandmarkType']
        location = req['queryResult']['parameters']['Location']
        # Use the category type and location to retrieve data from your Django objects
        # ...
        response_text = "I recommend visiting {} in {}".format(category_type, location)
    else:
        response_text = "I'm sorry, I didn't understand that request."
    # Return a JSON response with the fulfillment text and entities
    response = {
        'fulfillmentText': response_text,
        'outputContexts': req['queryResult']['outputContexts']
    }
    return JsonResponse(response)


class DownloadMediaFolderView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        from django.http import FileResponse
        import os
        
        import tempfile
        import zipfile


        # Get the path to the media folder
        media_root = settings.MEDIA_ROOT

        # Zip the contents of the media folder into a temporary file
        zip_path = os.path.join(tempfile.gettempdir(), 'media.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(media_root):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, media_root))

        # Create a response with the temporary file as an attachment
        response = FileResponse(open(zip_path, 'rb'), as_attachment=True, filename='media.zip')

        # Set the content type to "application/zip"
        response['Content-Type'] = 'application/zip'

        return response