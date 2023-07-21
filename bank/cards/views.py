from rest_framework import viewsets
from rest_framework.response import Response
from .models import Card, Status
from .serializers import CardSerializer, CardSerializerUpdate
from rest_framework.decorators import action


class CardsViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return CardSerializerUpdate

        return CardSerializer


    def list(self, request):
        cards = Card.objects.filter(owner=request.user)

        if cards:
            data = [CardSerializer(card).data for card in cards]
        
            return Response(data)

        return Response({"error": "You don`t have any cards"})


    @action(methods=['get'], detail=True)
    def freeze(self, request, pk=None):
        if not pk:
            Response({'error': 'You need to enter a pk'})

        try:
            card = Card.objects.get(pk=pk)
        except:
            Response({'error': 'The object doesn`t exist'})

        card.status = Status.objects.get(pk=4)
        card.save()

        return Response(CardSerializer(card).data)


    @action(methods=['get'], detail=True)
    def reactivate(self, request, pk=None):
        if not pk:
            Response({'error': 'You need to enter a pk'})

        try:
            card = Card.objects.get(pk=pk)
        except:
            Response({'error': 'The object doesn`t exist'})

        card.status = Status.objects.get(pk=2)
        card.save()

        return Response(CardSerializer(card).data)
