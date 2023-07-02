from django.urls import path, include

from .views import(
    MaximiumEventsView,
    TourPackageListView,
    TourPackageView,
    UserTourPackageListView
)

urlpatterns = [

    path('tour_packages/',TourPackageListView.as_view()),
    path('tour_packages_created_by_me/',UserTourPackageListView.as_view(), name='user_tour_packages'),
    path('<str:language_code>/create_tour_package_events/',MaximiumEventsView.as_view()),
    path('tour_packages/<int:tour_package_id>/',TourPackageView.as_view()),
    # path('<str:lang_code>/<int:event_id>/tickets/',TicketsForSpecificLandmarkEvent.as_view())

]
