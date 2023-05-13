from django.urls import path, include

from .views import(
    TourismCategoriesListView,
    TourismCategoryView,
    TourismCategoriesCoreListView
)

urlpatterns = [

    path('<str:lang_code>/tourism_categories/',TourismCategoriesListView.as_view(), name='tourism_categories'),
    path('<str:lang_code>/tourism_categories/<int:category_id>/',TourismCategoryView.as_view()),
    path('tourism_categories/',TourismCategoriesCoreListView.as_view())
]
