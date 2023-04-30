
from django.urls import path, include
from .router import router



urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('', include((router.urls, 'app_name'), namespace='instance_name')),
    # path('<str:lang_code>/governorates/',
    #      GovernoratesView.as_view(), name='governorates')
]
