from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CardSerializer, CardSerializerUpdate
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Card, Status
from .permissions import IsOwner
from .tasks import activate


class CardsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner, IsAuthenticated]
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


    @action(methods=['get'], detail=True, permission_classes=[IsOwner, IsAuthenticated])
    def freeze(self, request, pk=None):
        if not pk:
            Response({'error': 'You need to enter a pk'})

        try:
            card = Card.objects.get(pk=pk)
        except:
            Response({'error': 'The object doesn`t exist'})

        if not (request.user.is_authenticated and request.user == card.owner):
            return Response({'error': 'It`s not your object'})

        card.status = Status.objects.get(pk=4)
        card.save()

        return Response(CardSerializer(card).data)


    @action(methods=['get'], detail=True, permission_classes=[IsOwner, IsAuthenticated])
    def reactivate(self, request, pk=None):
        if not pk:
            Response({'error': 'You need to enter a pk'})

        try:
            card = Card.objects.get(pk=pk)
        except:
            Response({'error': 'The object doesn`t exist'})

        if not (request.user.is_authenticated and request.user == card.owner):
            return Response({'error': 'It`s not your object'})

        activate.apply_async(args=[int(pk)])
        
        #CardSerializer(card).data
        return Response({'Warning': 'Status will be changed in 2 minutes'})
