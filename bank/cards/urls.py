from django.urls import path, include
from rest_framework import routers
from .views import CardsViewSet

router = routers.SimpleRouter()
router.register(r'cards', CardsViewSet)


urlpatterns = [
	path('api/v1/', include(router.urls)) 
]