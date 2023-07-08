from django.urls import path, include
# from rest_framework import routers


from .views import (
    ImageListView,
    ImageView,
    ChatbotView,
    DownloadMediaFolderView,
    dialogflow_webhook
)


urlpatterns = [
    path('images/',ImageListView.as_view()),
    path('images/<int:image_id>/',ImageView.as_view()),
    path('chatbot/',ChatbotView.as_view()),
    # path('chat/',dialogflow_webhook),
    path('download_media_folder/',DownloadMediaFolderView.as_view())
]
