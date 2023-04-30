from rest_framework import routers
from system.views import LanguageView
from users.views import UsersView
# system_router = routers.DefaultRouter()

# system_router.register(r'ar', GovernorateView, 'ar')


router = routers.DefaultRouter()
router.register(r'languages', LanguageView, 'language')
router.register(r'users', UsersView, 'user')
# router.registry.extend(system_router.registry)
