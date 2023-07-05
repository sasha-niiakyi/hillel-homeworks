from django.urls import path

from cards.views import CardsView


urlpatterns = [
	path('card/', CardsView.as_view(http_method_names=['get', 'post']) , name='card')
]