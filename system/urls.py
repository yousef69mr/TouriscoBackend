from django.urls import path, include
# from rest_framework import routers


from .views import (
    ImageListView,
    ImageView,
    ChatbotView
)


urlpatterns = [
    path('images/',ImageListView.as_view()),
    path('images/<int:image_id>/',ImageView.as_view()),
    path('chatbot/',ChatbotView.as_view())

]
