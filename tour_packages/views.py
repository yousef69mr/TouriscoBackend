
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,IsAuthenticated)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from landmark_events.models import LandmarkEvent
from tickets.models import Ticket


from .serializers import (
    TourPackageSerializer
)
from .models import (
    TourPackage
   
)
# Create your views here.


class TourPackageView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'landmark_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, tour_package_id, format=None):

        tour_package = get_object_or_404(TourPackage, id=tour_package_id)
        
        print(tour_package)
        try:
            serializer = TourPackageSerializer(tour_package)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)



class UserTourPackageListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        # user = get_object_or_404(User,id=request.user.id)
        packages = TourPackage.objects.all(user_created_by=request.user.id)
        # print(governorates)
        serializer = TourPackageSerializer(packages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
        

class TourPackageListView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):

        packages = TourPackage.objects.all()
        # print(governorates)
        serializer = TourPackageSerializer(packages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):

        try:
            copy_data = request.data.copy()
            copy_data['user_created_by'] =  request.user.id
            serializer = TourPackageSerializer(data=copy_data)
            if serializer.is_valid():
                serializer.save()
                # print('\n\n\ni\n\n\n')

            return Response(serializer, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MaximiumEventsView(APIView):
    def post(self , request):
        tickets = Ticket.objects.all()
        
        # # Import necessary libraries
        # import pandas as pd
        # from sklearn.linear_model import LinearRegression
        # from sklearn.feature_selection import train_test_split
        # from sklearn.metrics import r2_score

        # # Define the Django models for ticket and event objects

        # # Load the data from the Django database
        # event_objects = LandmarkEvent.objects.all().values('start_time', 'end_time', 'location', 'ticket_object__price')
        # data = pd.DataFrame.from_records(event_objects)

        # # Define the input and output variables
        # X = data.drop('ticket_object__price', axis=1)
        # y = data['ticket_object__price']

        # # Filter the data by time interval
        # start_time = '2022-01-01 00:00:00' # Example start time
        # end_time = '2022-12-31 23:59:59' # Example end time
        # X = X[(X['start_time'] >= start_time) & (X['end_time'] <= end_time)]
        # y = y[X.index]

        # # Split the data into training and validation sets
        # X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # # Train the linear regression model
        # model = LinearRegression()
        # model.fit(X_train, y_train)

        # # Evaluate the model on the validation set
        # y_pred = model.predict(X_val)
        # r2_score = r2_score(y_val, y_pred)
        # print("R-squared score:", r2_score)

        # # Predict the maximum number of event objects that satisfy the given ticket price sum and time interval
        # price_sum = 1000 # Example ticket price sum
        # event_objects = X.copy()
        # event_objects['predicted_ticket_price'] = model.predict(X)
        # event_objects['ticket_price_sum'] = event_objects['predicted_ticket_price'].cumsum()
        # event_objects = event_objects[event_objects['ticket_price_sum']<=price_sum]
        # event_objects = event_objects[(event_objects['start_time'] >= start_time) & (event_objects['end_time'] <= end_time)]
        # print(event_objects)
        # max_num = len(event_objects)
        # print("Maximum number of event objects that satisfy the ticket price sum and time interval:", max_num)