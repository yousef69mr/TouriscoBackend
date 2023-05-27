from django.urls import path

from .views import(
    ReviewImagesView,
    ReviewListView,
    ReviewView
)

urlpatterns = [

    # path('<str:lang_code>/reviews/',TicketsView.as_view()),
    # path('<str:lang_code>/<int:event_id>/reviews/',TicketsForSpecificLandmarkEvent.as_view(), name='tickets'),
    path('reviews/<int:review_id>/',ReviewView.as_view()),
    path('reviews/',ReviewListView.as_view()),
    # path('<str:lang_code>/reviews/<int:ticket_id>/',TicketView.as_view()),
    path('review_images/<int:review_id>/',ReviewImagesView.as_view()),
    
    # path('<str:lang_code>/<int:event_id>/tickets/',TicketsForSpecificLandmarkEvent.as_view())

]
