from django.urls import path

from cards.views import createview, showview, homeview


urlpatterns = [
	path('create/',  createview, name='create_card'),
	path('show/', showview, name='show_card'),
	path('', homeview, name='home_card'),
]