from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health_check, chat, AuthViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health-check'),
    path('chat/', chat, name='chat'),
]
