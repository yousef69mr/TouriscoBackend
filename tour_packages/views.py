
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,IsAuthenticated)


from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import QueryDict
from datetime import date,datetime
from django.utils import timezone
from landmark_events.models import LandmarkEvent
from landmark_events.serializers import EventSerializer
from tickets.models import Ticket
from users.models import User
from categories.models import TourismCategory

from .serializers import (
    TourPackageSerializer,
    TourPackageTourismCategorySerializer,
    TourPackageTicketSerializer,
    TourPackageLandmarkEventSerializer
)
from .models import (
    TourPackage
   
)
# Create your views here.

class IncreaseTourPackageViewsView(APIView):
    def post(self, request, tour_package_id, format=None):
        package = get_object_or_404(TourPackage, id=tour_package_id)
        print(package)
        try:
            package.increase_views()
            package.save()
            return Response({'message':"increased successfully"},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TourPackageView(APIView):
    # queryset = LandmarkLanguageBased.objects.all()
    # serializer_class = LandmarksSerializer
    lookup_field = ['lang_code', 'tour_package_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, tour_package_id, format=None):

        tour_package = get_object_or_404(TourPackage, id=tour_package_id)
        
        print(tour_package)
        try:
            tour_package.increase_views()
            tour_package.save()
            serializer = TourPackageSerializer(tour_package)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, tour_package_id, format=None):
        tour_package = get_object_or_404(TourPackage, id=tour_package_id)
        try:
            serializer = TourPackageSerializer(tour_package, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, tour_package_id, format=None):
        tour_package = get_object_or_404(TourPackage, id=tour_package_id)
        tour_package.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




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
            # create package algorithm

            package_data = generate_tourpackage_data(request)
            # print(package_data)

            serializer = TourPackageSerializer(data=package_data)
            if serializer.is_valid():
                serializer.save()
                # print('\n\n\ni\n\n\n')
                package = TourPackage.objects.get(id=serializer.data.get('id'))
                # package = TourPackage.objects.get(id=1)

                tourism_categories = package_data.get('tourism_categories')
                tickets = package_data.get('tickets')
                events = package_data.get('events')
                # print(tourism_categories)
                for category in tourism_categories:
                    tourism_data = QueryDict(mutable=True)
                    # print(category)
                    tourism_data['tourism_category'] = category
                    tourism_data['tourpackage'] = package.id
                    category_serializer = TourPackageTourismCategorySerializer(data=tourism_data)
                    if category_serializer.is_valid():
                        category_serializer.save()

                for ticket in tickets:
                    ticket_data = QueryDict(mutable=True)
                    # print(category)
                    ticket_data['ticket'] = ticket
                    ticket_data['tourpackage'] = package.id
                    ticket_serializer = TourPackageTicketSerializer(data=ticket_data)
                    if ticket_serializer.is_valid():
                        ticket_serializer.save()

                for event in events:
                    event_data = QueryDict(mutable=True)
                    # print(category)
                    event_data['event'] = event
                    event_data['tourpackage'] = package.id
                    event_serializer = TourPackageLandmarkEventSerializer(data=event_data)
                    if event_serializer.is_valid():
                        event_serializer.save()

                package = TourPackage.objects.get(id=serializer.data.get('id'))
                # package = TourPackage.objects.get(id=2)
                package_serializer = TourPackageSerializer(package)

                return Response(package_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# sliding window technique has a time complexity of O(nlogn)
def max_tickets(objects, target):
    n = len(objects)
    objects = sorted(objects, key=lambda obj: obj.price)
    i, j, sum_price = 0, 0, 0
    max_tickets = 0
    ticket_ids = []
    while j < n:
        if sum_price + objects[j].price <= target:
            sum_price += objects[j].price
            j += 1
            max_tickets = max(max_tickets, j-i)
        else:
            sum_price -= objects[i].price
            i += 1
        if sum_price <= target and max_tickets == j-i:
           ticket_ids = [obj.id for obj in objects[i:j]]
    return ticket_ids


def generate_tourpackage_data(request):
    arabic_countries = ['AE', 'BH', 'DJ', 'DZ', 'EG', 'IQ', 'JO', 'KW', 'LB', 'LY', 'MA', 'MR', 'OM', 'PS', 'QA', 'SA', 'SD', 'SO', 'SY', 'TN', 'YE']
            
    # if request.user:
    #     user = User.objects.get(id=request.user.id)
    # if 
    user = User.objects.get(id=request.user.id)
    request_data_copy = request.data.copy()
    print(request_data_copy)
    budget_target = float(request_data_copy.get('budget_target',0))
    print(type(budget_target))
    today = date.today()  # get current date as a date object
    # default_start_date = datetime.combine(today, datetime.min.time())  # convert to datetime object with minimum time
    if user.nationality == 'EG':
        if user.birth_date:
            if (today-user.birth_date).days >= 21:
                ticket_class_name = 'Egyptian'
            else:
                ticket_class_name ='Student'
        else:
            ticket_class_name ='Egyptian'

    elif user.nationality in arabic_countries:
        if user.birth_date:
            if (today-user.birth_date).days >= 21:
                ticket_class_name = 'Arab'
            else:
                ticket_class_name ='Student'
        else:
            ticket_class_name ='Arab'
        
    else:
        if user.birth_date:
            if (today-user.birth_date).days >= 21:
                ticket_class_name = 'Foreigner'
            else:
                ticket_class_name ='Foreigner_Student'
        else:
            ticket_class_name ='Foreigner'
        
    preffered_tourism = request_data_copy.get('tourism_categories',[])
    if len(preffered_tourism)==0:
        preffered_tourism = TourismCategory.objects.all().values_list('id',flat=True)

    print(preffered_tourism)

    startDate = request_data_copy.get('start_date',timezone.now())
    endDate = request_data_copy.get('end_date',None)

    if endDate is None:
        raise ValueError('end_date is required field')

    
    print(startDate)
    print(endDate)

    print(str(endDate))
    print(type(endDate))

    


    # convert the string objects to datetime objects
    # startDate = datetime.strptime(str(startDate), '%Y-%m-%d')
    # endDate = datetime.strptime(str(endDate), '%Y-%m-%d')
    # print('dsd')
    # package_duration = (endDate - startDate)
    # print(package_duration)

    tickets_for_user = Ticket.objects.filter(ticketClassObject__name=ticket_class_name,eventObject__start_date__lte=startDate,eventObject__end_date__gte=endDate)
    # tickets_for_user = Ticket.objects.all()
    print(tickets_for_user)

    # step 2 : deal with tourism categories
    prefferd_tickets = tickets_for_user.filter(eventObject__landmarkObject__tourism_categories__in = preffered_tourism).distinct()
    
    # step 3 : deal with target budget 
    

    max_num_tickets_ids = max_tickets(prefferd_tickets, budget_target)

    print(max_num_tickets_ids)
    # get budget of selected tickets
    selected_tickets = Ticket.objects.filter(id__in=max_num_tickets_ids)
    # print("preferred_tickets",selected_tickets)


    total_price = selected_tickets.aggregate(Sum('price'))['price__sum']

    # if no selected_tickets 
    if total_price is None:
        total_price = 0

    # print(total_price)
    # event_ids = selected_tickets.values_list('eventObject',flat=True).distinct()

    # check if their is a chance to add any tickets

    if total_price < budget_target:
        other_tourism_tickets=tickets_for_user.exclude(eventObject__landmarkObject__tourism_categories__in = preffered_tourism).distinct()
        # print(other_tourism_tickets)
        if len(other_tourism_tickets)>0:
            remaining_budget = budget_target - total_price

            max_num_remaining_tickets_ids = max_tickets(other_tourism_tickets, remaining_budget)
            # print(max_num_tickets_ids)
            # print(max_num_remaining_tickets_ids)
            
            tickets_ids = max_num_tickets_ids + max_num_remaining_tickets_ids
            print(tickets_ids)
            selected_tickets = Ticket.objects.filter(id__in=tickets_ids)

            


    # step 4 : get all events
    # selected_tickets = Ticket.objects.filter(id__in=max_num_tickets_ids)
    
    event_ids = selected_tickets.values_list('eventObject',flat=True).distinct()
    package_tourism_categories = selected_tickets.values_list('eventObject__landmarkObject__tourism_categories',flat=True).distinct()
    print(package_tourism_categories)

    package_tourism_categories_ids = [category for category in package_tourism_categories]
    # print(package_tourism_categories_ids)
    tickets_list = selected_tickets.values_list('id',flat=True).distinct()
    # print(event_ids)
    # events = LandmarkEvent.objects.filter(id__in=event_ids)
    title = request_data_copy.get('title',None)
    if title is None or len(title)==0:
        title = 'Tourisco'

    package_data = QueryDict(mutable=True)
    package_data['title'] = title
    package_data['package_maximium_budget'] = budget_target
    package_data['events'] = list(event_ids)
    package_data['tickets'] = list(tickets_list)
    package_data['user_created_by'] = user.id
    package_data['tourism_categories'] = package_tourism_categories_ids
    package_data['start_date'] = startDate
    package_data['end_date'] = endDate

    return package_data
    # language_events = LandmarkEventLanguageBased.objects.filter(lang__code=language_code,eventObject__in=event_ids)
    # events_serializer = EventsSerializer(language_events,many=True)


class MaximiumEventsView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def post(self ,request,language_code):
        
        # try:
        #     arabic_countries = ['AE', 'BH', 'DJ', 'DZ', 'EG', 'IQ', 'JO', 'KW', 'LB', 'LY', 'MA', 'MR', 'OM', 'PS', 'QA', 'SA', 'SD', 'SO', 'SY', 'TN', 'YE']
            
        #     # if request.user:
        #     #     user = User.objects.get(id=request.user.id)
        #     # if 
        #     user = User.objects.get(id=1)
        #     budget_target = request.data.pop('budget_target',0)
        #     today = date.today()  # get current date as a date object
        #     # default_start_date = datetime.combine(today, datetime.min.time())  # convert to datetime object with minimum time
        #     if user.nationality == 'EG':
        #         if user.birth_date:
        #             if (today-user.birth_date).days >= 21:
        #                 ticket_class_name = 'Egyptian'
        #             else:
        #                 ticket_class_name ='Student'
        #         else:
        #             ticket_class_name ='Egyptian'

        #     elif user.nationality in arabic_countries:
        #         if user.birth_date:
        #             if (today-user.birth_date).days >= 21:
        #                 ticket_class_name = 'Arab'
        #             else:
        #                 ticket_class_name ='Student'
        #         else:
        #             ticket_class_name ='Arab'
                
        #     else:
        #         if (today-user.birth_date).days >= 21:
        #             ticket_class_name = 'Foreigner'
        #         else:
        #             ticket_class_name ='Foreigner_Student'
                
        #     preffered_tourism = request.data.pop('tourism_categories',[])
        #     if len(preffered_tourism)==0:
        #         preffered_tourism = TourismCategory.objects.all().values_list('id',flat=True)

        #     print(preffered_tourism)

        #     startDate = request.data.pop('start_date',timezone.now())
        #     endDate = request.data.pop('end_date',None)

        #     if endDate is None:
        #         raise ValueError('end_date is required field')

            
        #     print(startDate)
        #     print(endDate)

        #     # convert the string objects to datetime objects
        #     startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        #     endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        #     package_duration = (endDate - startDate)
        #     print(package_duration)

        #     tickets_for_user = Ticket.objects.filter(ticketClassObject__name=ticket_class_name,eventObject__start_date__lte=startDate,eventObject__end_date__gte=endDate)
        #     # tickets_for_user = Ticket.objects.all()
        #     # print(tickets_for_user)

        #     # step 2 : deal with tourism categories
        #     prefferd_tickets = tickets_for_user.filter(eventObject__landmarkObject__tourism_categories__in = preffered_tourism).distinct()
        #     # tickets = Ticket.objects.all()
        #     # print(prefferd_tickets)
        #     # if len(prefferd_tickets)==0:
        #     #     other_tourism_tickets=tickets_for_user.exclude(eventObject__landmarkObject__tourism_categories__in = preffered_tourism).distinct()
        #     #     # print()
        #     #     if len(other_tourism_tickets)>0:
        #     #         # remaining_budget = budget_target - 0

        #     #         tickets_ids = max_tickets(other_tourism_tickets, budget_target)
        #     #         # tickets_ids = max_num_tickets_ids.extend(max_num_remaining_tickets_ids)
        #     #         selected_tickets = Ticket.objects.filter(id__in=tickets_ids)
        #     # ticket_prices = [ticket.price for ticket in tickets]
        #     # print(ticket_prices)

        #     # step 3 : deal with target budget 
           

        #     max_num_tickets_ids = max_tickets(prefferd_tickets, budget_target)

        #     # print(max_num_tickets_ids)
        #     # get budget of selected tickets
        #     selected_tickets = Ticket.objects.filter(id__in=max_num_tickets_ids)
        #     # print("preferred_tickets",selected_tickets)


        #     total_price = selected_tickets.aggregate(Sum('price'))['price__sum']

        #     # if no selected_tickets 
        #     if total_price is None:
        #         total_price = 0

        #     # print(total_price)
        #     # event_ids = selected_tickets.values_list('eventObject',flat=True).distinct()

        #     # check if their is a chance to add any tickets

        #     if total_price < budget_target:
        #         other_tourism_tickets=tickets_for_user.exclude(eventObject__landmarkObject__tourism_categories__in = preffered_tourism).distinct()
        #         # print(other_tourism_tickets)
        #         if len(other_tourism_tickets)>0:
        #             remaining_budget = budget_target - total_price

        #             max_num_remaining_tickets_ids = max_tickets(other_tourism_tickets, remaining_budget)
        #             # print(max_num_tickets_ids)
        #             # print(max_num_remaining_tickets_ids)
                    
        #             tickets_ids = max_num_tickets_ids + max_num_remaining_tickets_ids
        #             # print(tickets_ids)
        #             selected_tickets = Ticket.objects.filter(id__in=tickets_ids)

                    


        #     # step 4 : get all events
        #     # selected_tickets = Ticket.objects.filter(id__in=max_num_tickets_ids)
        #     event_ids = selected_tickets.values_list('eventObject',flat=True).distinct()
        #     package_tourism_categories = selected_tickets.values_list('eventObject__landmarkObject__tourism_categories',flat=True).distinct()
        #     print(package_tourism_categories)
        #     # print(event_ids)
        #     # events = LandmarkEvent.objects.filter(id__in=event_ids)
        #     language_events = LandmarkEventLanguageBased.objects.filter(lang__code=language_code,eventObject__in=event_ids)
        #     events_serializer = EventsSerializer(language_events,many=True)
            
        #     return Response(events_serializer.data, status=status.HTTP_200_OK)
            
            
        #     # # Import necessary libraries
        #     # import pandas as pd
        #     # from sklearn.linear_model import LinearRegression
        #     # from sklearn.feature_selection import train_test_split
        #     # from sklearn.metrics import r2_score

        #     # # Define the Django models for ticket and event objects

        #     # # Load the data from the Django database
        #     # event_objects = LandmarkEvent.objects.all().values('start_time', 'end_time', 'location', 'ticket_object__price')
        #     # data = pd.DataFrame.from_records(event_objects)

        #     # # Define the input and output variables
        #     # X = data.drop('ticket_object__price', axis=1)
        #     # y = data['ticket_object__price']

        #     # # Filter the data by time interval
        #     # start_time = '2022-01-01 00:00:00' # Example start time
        #     # end_time = '2022-12-31 23:59:59' # Example end time
        #     # X = X[(X['start_time'] >= start_time) & (X['end_time'] <= end_time)]
        #     # y = y[X.index]

        #     # # Split the data into training and validation sets
        #     # X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        #     # # Train the linear regression model
        #     # model = LinearRegression()
        #     # model.fit(X_train, y_train)

        #     # # Evaluate the model on the validation set
        #     # y_pred = model.predict(X_val)
        #     # r2_score = r2_score(y_val, y_pred)
        #     # print("R-squared score:", r2_score)

        #     # # Predict the maximum number of event objects that satisfy the given ticket price sum and time interval
        #     # price_sum = 1000 # Example ticket price sum
        #     # event_objects = X.copy()
        #     # event_objects['predicted_ticket_price'] = model.predict(X)
        #     # event_objects['ticket_price_sum'] = event_objects['predicted_ticket_price'].cumsum()
        #     # event_objects = event_objects[event_objects['ticket_price_sum']<=price_sum]
        #     # event_objects = event_objects[(event_objects['start_time'] >= start_time) & (event_objects['end_time'] <= end_time)]
        #     # print(event_objects)
        #     # max_num = len(event_objects)
        #     # print("Maximum number of event objects that satisfy the ticket price sum and time interval:", max_num)
        # # except ValueError as e:
        try:
            data = generate_tourpackage_data(request)
            print(data)
            events = LandmarkEvent.objects.filter(id__in=data['events'])
            # language_events = LandmarkEventLanguageBased.objects.filter(lang__code=language_code,eventObject__in=event_ids)
            events_serializer = EventSerializer(events,many=True)
            
            return Response(events_serializer.data, status=status.HTTP_200_OK)
        #     return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)