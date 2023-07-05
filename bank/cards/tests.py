from django.test import TestCase
from cards.models import Card
from django.urls import reverse


class CardsTest(TestCase):

	def test_get_card(self):
		# given
		card = Card(number=1111222233334444, expir_date='2025-11-01', cvv=456)
		card.save()
		url = reverse('card') + '?number=1111222233334444'

		# when
		response = self.client.get(url).json()
		print(card.date_of_issue)

		# then
		self.assertEquals(response, {'card': {'number': card.number,
                                      'expir_date': card.expir_date,
                                      'cvv': card.cvv,
                                      'date_of_issue': str(card.date_of_issue), 
                                      'user_id': str(card.user_id),
                                      'status': card.status}})


	def test_is_valid_false(self):
		card = Card(number=1111222233334443, expir_date='2025-11-01', cvv=456)

		result = card.is_valid()
		self.assertEquals(result, False)


	def test_is_valid_true(self):
		card = Card(number=2000000000000006, expir_date='2025-11-01', cvv=456)

		result = card.is_valid()
		self.assertEquals(result, True)

