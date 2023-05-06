from django.urls import path, include

from .views import(
LandmarkEventCoreListView,
LandmarkEventListView,
LandmarkEventView
)

urlpatterns = [
    
    #event
    path('<str:lang_code>/<int:landmark_id>/events/',
         LandmarkEventListView.as_view(), name='events'),
    # path('<str:lang_code>/events/', LandmarkEventListView.as_view(), name='events'),
    path('events/', LandmarkEventCoreListView.as_view(), name="event"),
    path('<str:lang_code>/<int:landmark_id>/events/<int:event_id>/', LandmarkEventView.as_view(), name='event'),


]
