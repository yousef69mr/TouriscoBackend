from django.urls import path, include

from .views import(
    TicketsView
)

urlpatterns = [

    path('<str:lang_code>/<int:landmark_id>/<int:event_id>/tickets/',
         TicketsView.as_view(), name='tickets')

]
