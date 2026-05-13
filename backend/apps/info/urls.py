from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.info.views import SouvenirViewSet, AppViewSet, AdvertisementViewSet, TranslateView

router = DefaultRouter()
router.register('souvenirs', SouvenirViewSet, basename='souvenir')
router.register('apps', AppViewSet, basename='app')
router.register('advertisements', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('translate/', TranslateView.as_view(), name='translate'),
] + router.urls
