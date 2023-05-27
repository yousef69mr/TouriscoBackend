from django.urls import path, include

from .views import (
    LandmarkCoreListView,
    LandmarkListView,
    LandmarkView,
    LandmarkInSpecificGovernorate,
    LandmarkImagesView,
    LandmarkReviewsView
)

urlpatterns = [

     path('<str:lang_code>/governorate_landmarks/<int:governorate_id>/',LandmarkInSpecificGovernorate.as_view()),
     # landmarks
     path('<str:lang_code>/landmarks/',LandmarkListView.as_view(), name='landmarks'),
     path('<str:lang_code>/landmarks/<int:landmark_id>/',LandmarkView.as_view(), name="landmark"),
     path('landmarks/', LandmarkCoreListView.as_view(), name="landmarks"),
     path('landmark_images/<int:landmark_id>/',LandmarkImagesView.as_view()),
     path('landmark_reviews/<int:landmark_id>/',LandmarkReviewsView.as_view())

]
