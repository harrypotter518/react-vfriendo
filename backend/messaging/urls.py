from rest_framework.routers import DefaultRouter

from .views import MessagesViewSet

router = DefaultRouter()
router.register(r'messages', MessagesViewSet, basename='message')

urlpatterns = router.urls
