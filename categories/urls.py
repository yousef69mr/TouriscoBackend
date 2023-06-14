from django.urls import path, include

from .views import(
    TourismCategoriesListView,
    TourismCategoryView,
    TourismCategoriesCoreListView,
    TypeCategoriesListView,
    TypeCategoryView,
    TypeCategoriesCoreListView,
    TicketClassCategoryView,
    TicketClassCategoriesListView,
    TicketClassCategoriesCoreListView
)

urlpatterns = [

    path('<str:lang_code>/tourism_categories/',TourismCategoriesListView.as_view(), name='tourism_categories'),
    path('<str:lang_code>/tourism_categories/<int:category_id>/',TourismCategoryView.as_view()),
    path('tourism_categories/',TourismCategoriesCoreListView.as_view()),
    path('<str:lang_code>/type_categories/',TypeCategoriesListView.as_view(), name='type_categories'),
    path('<str:lang_code>/type_categories/<int:category_id>/',TypeCategoryView.as_view()),
    path('type_categories/',TypeCategoriesCoreListView.as_view()),
    path('<str:lang_code>/ticket_class_categories/',TicketClassCategoriesListView.as_view(), name='ticket_class_categories'),
    path('<str:lang_code>/ticket_class_categories/<int:category_id>/',TicketClassCategoryView.as_view()),
    path('ticket_class_categories/',TicketClassCategoriesCoreListView.as_view())
]
