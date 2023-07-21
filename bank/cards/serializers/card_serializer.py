from rest_framework import serializers
from cards.models import Card


class CardSerializer(serializers.ModelSerializer):
	owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = Card
		fields = ('__all__')
		read_only_fields = ['date_of_issue', 'owner', 'status']