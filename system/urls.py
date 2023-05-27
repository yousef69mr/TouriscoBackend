from django.urls import path, include
# from rest_framework import routers


from .views import (
    ImageListView,
    ImageView
)


urlpatterns = [
    path('images/',ImageListView.as_view()),
    path('images/<int:image_id>/',ImageView.as_view()),

]
