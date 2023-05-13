from django.urls import path, include

from .views import(
LandmarkEventCoreListView,
LandmarkEventListView,
LandmarkEventView
)

urlpatterns = [
    
    #event
    path('<str:lang_code>/<int:landmark_id>/landmark_events/',
         LandmarkEventListView.as_view(), name='landmark_events'),
    # path('<str:lang_code>/events/', LandmarkEventListView.as_view(), name='events'),
    path('landmark_events/', LandmarkEventCoreListView.as_view(), name="event"),
    path('<str:language_id>/landmark_events/', LandmarkEventCoreListView.as_view(), name="event"),
    path('<str:lang_code>/landmark_events/<int:event_id>/', LandmarkEventView.as_view(), name='event'),


]
