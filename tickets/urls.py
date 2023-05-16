from django.urls import path, include

from .views import(
    TicketsView,
    TicketCoreListView,
    TicketView,
    TicketsForSpecificLandmarkEvent
)

urlpatterns = [

    path('<str:lang_code>/tickets/',TicketsView.as_view()),
    path('<str:lang_code>/<int:event_id>/tickets/',TicketsForSpecificLandmarkEvent.as_view(), name='tickets'),
    path('tickets/',TicketCoreListView.as_view()),
    path('<str:lang_code>/tickets/<int:ticket_id>/',TicketView.as_view()),
    # path('<str:lang_code>/<int:event_id>/tickets/',TicketsForSpecificLandmarkEvent.as_view())

]
