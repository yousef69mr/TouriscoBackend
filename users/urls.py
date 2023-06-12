from django.urls import path
from .views import (
    CreateUserView, 
    MyTokenObtainPairView,
    ActiveUserView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('create_user/', CreateUserView.as_view()),
    path('active_user/', ActiveUserView.as_view()),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
