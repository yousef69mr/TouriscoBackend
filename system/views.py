
from rest_framework import viewsets, status
from rest_framework.views import APIView
# from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import GoogleAPIError
import dialogflow

import os
from TouriscoBackend.settings import BASE_DIR

from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

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
        desired_language=request.POST.get('language_code','ar')
        input_text = request.POST.get('message','')
        input_text = translator.translate(text=input_text,dest=agent_language_code).text
        print(input_text)
        try:
            
            GOOGLE_AUTHENTICATION_FILE_NAME = "tourisco-494f889ff6ac.json"
            current_directory = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
            print(path)
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
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    #text = "this is as test"
    text = user_input

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        query_params=query_params
    )

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))

    return response
    


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