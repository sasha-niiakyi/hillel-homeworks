from django.template.loader import render_to_string
from django.test import TestCase
from cards.models import Card
from django.urls import reverse
import json


class CardsTest(TestCase):

	def test_get_card(self):
		# given
		create_card = Card(number=1111222233334444, expir_date='2025-11-01', cvv=456)
		create_card.save()

		card = Card.objects.filter(number=1111222233334444).first()

		url = reverse('show_card') + '?number=1111222233334444'

		# when
		response = self.client.get(url)

		actual_template = 'cards/show.html'
		data = {'title': 'Show card', 'card': card}

		expected_result = render_to_string(actual_template, data)

		# then
		self.assertEquals(expected_result, response.content.decode('utf-8'))


	# def test_post_card(self):
	# 	# given
	# 	data = json.dumps({
	# 						"number": 1111222233334455,
	# 						"expir_date": "2025-11-01",
	# 						"cvv": 123
	# 					})

	# 	url = reverse('card')

	# 	# when
	# 	response = self.client.post(url, data=data, content_type='application/json')

	# 	card = Card.objects.filter(number=1111222233334455)[0]

	# 	# then
	# 	self.assertEquals(response.json(), {'card': {'number': card.number,
	# 	                                      'expir_date': str(card.expir_date),
	# 	                                      'cvv': card.cvv,
	# 	                                      'date_of_issue': str(card.date_of_issue), 
	# 	                                      'user_id': str(card.user_id),
	# 	                                      'status': card.status}})


	def test_is_valid_false(self):
		card = Card(number=1111222233334443, expir_date='2025-11-01', cvv=456)

		result = card.is_valid()
		self.assertEquals(result, False)


	def test_is_valid_true(self):
		card = Card(number=2000000000000006, expir_date='2025-11-01', cvv=456)

		result = card.is_valid()
		self.assertEquals(result, True)

