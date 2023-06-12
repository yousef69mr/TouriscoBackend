from django.urls import path, include

from .views import (
    LandmarkCoreListView,
    LandmarkListView,
    LandmarkView,
    LandmarkInSpecificGovernorateView,
    LandmarkWithSpecificTourismCategoryView,
    LandmarkWithSpecificTypeCategoryView,
    LandmarkImagesView,
    LandmarkReviewsView
)

urlpatterns = [

     path('<str:lang_code>/governorate_landmarks/<int:governorate_id>/',LandmarkInSpecificGovernorateView.as_view()),
     path('<str:lang_code>/tourism_category_landmarks/<int:tourism_category_id>/',LandmarkWithSpecificTourismCategoryView.as_view()),
     path('<str:lang_code>/type_category_landmarks/<int:type_category_id>/',LandmarkWithSpecificTypeCategoryView.as_view()),
     # landmarks
     path('<str:lang_code>/landmarks/',LandmarkListView.as_view(), name='landmarks'),
     path('<str:lang_code>/landmarks/<int:landmark_id>/',LandmarkView.as_view(), name="landmark"),
     path('landmarks/', LandmarkCoreListView.as_view(), name="landmarks"),
     path('landmark_images/<int:landmark_id>/',LandmarkImagesView.as_view()),
     path('landmark_reviews/<int:landmark_id>/',LandmarkReviewsView.as_view())

]
