import json
import uuid
from datetime import datetime

from django.contrib.auth.models import Permission, User
from rest_framework.test import APITestCase
from django.urls import reverse

from cards.models import Card, Status
from cards.serializers import CardSerializer


class CardsTest(APITestCase):

	def test_APIList(self):
		user = User.objects.create_user('testuser', password='test')

		card = Card.objects.create(owner=user, number=1111_1111_1111_1111,
									expir_date='2025-03-01', cvv=911)

		# add to db status
		for s_id, stat in [(1, 'new'), (2, 'active'), (3, 'blocked'), (4, 'freeze')]:
			status = Status(s_id, stat)
			status.save()

		url = reverse('card-list')

		expected_result = [
			{
				"number": card.number,
				"name": card.name,
				"expir_date": card.expir_date,
				"cvv": card.cvv,
				"date_of_issue": str(card.date_of_issue),
				"user_id": str(card.user_id),
				"status": card.status.id
			}
		]

		self.client.login(username=user.username, password='test')

		response = self.client.get(url).json()

		#create another user

		user2 = User.objects.create_user('testuser2', password='test2')
		self.client.login(username=user2.username, password='test2')
		response2 = self.client.get(url).json()
		expected_result2 = {
				'error': 'You don`t have any cards'
			}

		self.assertEqual(
			response,
			expected_result
		)
		self.assertEqual(
			response2,
			expected_result2
		)

	def test_APICreate(self):
		user = User.objects.create_user('testuser', password='test')

		# add to db status
		for i, j in [(1, 'new'), (2, 'active'), (3, 'blocked'), (4, 'freeze')]:
			status = Status(i, j)
			status.save()

		url = reverse('card-list')

		self.client.login(username=user.username, password='test')

		data = {
			"number": 1111_1111_1111_1111,
			"expir_date": "2025-03-01",
			"cvv": 911
		}

		response = self.client.post(url, data=data).json()

		expected_result = response | {'owner': user.id}

		card = Card.objects.filter(number=data['number']).first()

		result = CardSerializer(card).data | {'owner': card.owner.id}

		#create anonimus
		#second test
		self.client.force_authenticate(user=None)
		response2 = self.client.post(url, data=data).json()
		expected_result2 = {
			"detail": "Authentication credentials were not provided."
		}

		self.assertEqual(
			result,
			expected_result
		)
		self.assertEqual(
			response2,
			expected_result2
		)


	def test_APIDetail(self):
		user = User.objects.create_user('testuser', password='test')
		user2 = User.objects.create_user('testuser2', password='test2')

		card = Card.objects.create(owner=user, number=1111_1111_1111_1111,
									expir_date='2025-03-01', cvv=911)

		# add to db status
		for s_id, stat in [(1, 'new'), (2, 'active'), (3, 'blocked'), (4, 'freeze')]:
			status = Status(s_id, stat)
			status.save()

		url = reverse('card-detail', args=[card.number])

		expected_result = {
			"number": card.number,
			"name": card.name,
			"expir_date": card.expir_date,
			"cvv": card.cvv,
			"date_of_issue": str(card.date_of_issue),
			"user_id": str(card.user_id),
			"status": card.status.id
		}

		self.client.login(username=user.username, password='test')

		response = self.client.get(url).json()

		#second test
		self.client.login(username=user2.username, password='test2')
		response2 = self.client.get(url).json()
		expected_result2 = {
			"detail": "You do not have permission to perform this action."
		}

		self.assertEqual(
			response,
			expected_result
		)
		self.assertEqual(
			response2,
			expected_result2
		)


	def test_APIUpdate(self):
		user = User.objects.create_user('testuser', password='test')
		user2 = User.objects.create_user('testuser2', password='test2')

		card = Card.objects.create(owner=user, number=1111_1111_1111_1111,
									expir_date='2025-03-01', cvv=911)

		# add to db status
		for s_id, stat in [(1, 'new'), (2, 'active'), (3, 'blocked'), (4, 'freeze')]:
			status = Status(s_id, stat)
			status.save()

		url = reverse('card-detail', args=[card.number])

		data = {
			"name": "monobank",
			"cvv": 102
		}

		expected_result = {
			"number": card.number,
			"name": data['name'],
			"expir_date": card.expir_date,
			"cvv": data['cvv'],
			"date_of_issue": str(card.date_of_issue),
			"user_id": str(card.user_id),
			"status": card.status.id
		}

		self.client.login(username=user.username, password='test')

		response = self.client.patch(url, data=data).json()

		card = Card.objects.filter(number=1111_1111_1111_1111).first()

		result = CardSerializer(card).data


		#second test
		self.client.login(username=user2.username, password='test2')
		response2 = self.client.patch(url, data=data).json()
		expected_result2 = {
			"detail": "You do not have permission to perform this action."
		}

		self.assertEqual(
			result,
			expected_result
		)
		self.assertEqual(
			response2,
			expected_result2
		)


	def test_APIFreeze(self):
		user = User.objects.create_user('testuser', password='test')
		user2 = User.objects.create_user('testuser2', password='test2')

		card = Card.objects.create(owner=user, number=1111_1111_1111_1111,
									expir_date='2025-03-01', cvv=911)

		# add to db status
		for s_id, stat in [(1, 'new'), (2, 'active'), (3, 'blocked'), (4, 'freeze')]:
			status = Status(s_id, stat)
			status.save()

		url = reverse('card-freeze', args=[card.number])

		expected_result = {
			"number": card.number,
			"name": card.name,
			"expir_date": card.expir_date,
			"cvv": card.cvv,
			"date_of_issue": str(card.date_of_issue),
			"user_id": str(card.user_id),
			"status": 4
		}

		self.client.login(username=user.username, password='test')
		response = self.client.get(url).json()

		card = Card.objects.filter(number=1111_1111_1111_1111).first()
		result = CardSerializer(card).data


		#second test
		self.client.login(username=user2.username, password='test2')
		response2 = self.client.get(url).json()
		expected_result2 = {'error': 'It`s not your object'}

		self.assertEqual(
			result,
			expected_result
		)
		self.assertEqual(
			response2,
			expected_result2
		)


	def test_APIReactivate(self):
		user = User.objects.create_user('testuser', password='test')
		user2 = User.objects.create_user('testuser2', password='test2')

		card = Card.objects.create(owner=user, number=1111_1111_1111_1111,
									expir_date='2025-03-01', cvv=911)

		# add to db status
		for s_id, stat in [(1, 'new'), (2, 'active'), (3, 'blocked'), (4, 'freeze')]:
			status = Status(s_id, stat)
			status.save()

		url = reverse('card-reactivate', args=[card.number])

		expected_result = {
			"number": card.number,
			"name": card.name,
			"expir_date": card.expir_date,
			"cvv": card.cvv,
			"date_of_issue": str(card.date_of_issue),
			"user_id": str(card.user_id),
			"status": 2
		}

		self.client.login(username=user.username, password='test')
		response = self.client.get(url).json()

		card = Card.objects.filter(number=1111_1111_1111_1111).first()
		result = CardSerializer(card).data


		#second test
		self.client.login(username=user2.username, password='test2')
		response2 = self.client.get(url).json()
		expected_result2 = {'error': 'It`s not your object'}

		self.assertEqual(
			result,
			expected_result
		)
		self.assertEqual(
			response2,
			expected_result2
		)