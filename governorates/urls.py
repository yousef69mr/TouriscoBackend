from django.urls import path, include
from .views import(
    GovernorateCoreListView,
    GovernorateListView,
    GovernorateView
)



urlpatterns = [
#     # path('', include(system_router.urls)),
    path('<str:lang_code>/governorates/',
         GovernorateListView.as_view(), name='governorates'),
    path('governorates/',
         GovernorateCoreListView.as_view(), name='governorates_core'),
    path('<str:lang_code>/governorates/<int:governorate_id>/',
         GovernorateView.as_view(), name='governorate'),
]
