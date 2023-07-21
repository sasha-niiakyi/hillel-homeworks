from rest_framework import serializers
from cards.models import Card


class CardSerializerUpdate(serializers.ModelSerializer):
	class Meta:
		model = Card
		fields = ('name', 'cvv')
		read_only_fields = ['date_of_issue', 'owner', 'number']