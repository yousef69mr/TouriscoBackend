from django.urls import path, include
# from rest_framework import routers

from .views import (
    GovernorateListView,
    GovernorateCoreListView,
    GovernorateView,
    LandmarkEventView,
    LandmarkListView,
    LandmarkView,
    LandmarkCoreListView,
    TicketsView,
    LandmarkEventCoreListView,
    LandmarkEventListView
)


urlpatterns = [
    # path('', include(system_router.urls)),
    path('<str:lang_code>/governorates/',
         GovernorateListView.as_view(), name='governorates'),
    path('governorates/',
         GovernorateCoreListView.as_view(), name='governorates_core'),
    path('<str:lang_code>/governorates/<int:governorate_id>/',
         GovernorateView.as_view(), name='governorate'),
    # landmarks
    path('<str:lang_code>/landmarks/',
         LandmarkListView.as_view(), name='landmarks'),
    path('<str:lang_code>/landmarks/<int:landmark_id>/',
         LandmarkView.as_view(), name="landmark"),
    path('landmarks/', LandmarkCoreListView.as_view(), name="landmarks"),

    path('<str:lang_code>/<int:landmark_id>/events/',
         LandmarkEventListView.as_view(), name='events'),
    # path('<str:lang_code>/events/', LandmarkEventListView.as_view(), name='events'),
    path('events/', LandmarkEventCoreListView.as_view(), name="event"),

    path('<str:lang_code>/<int:landmark_id>/<int:event_id>/tickets/',
         TicketsView.as_view(), name='tickets')

]
