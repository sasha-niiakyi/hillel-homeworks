import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpRequest

from cards.models import Card


# class CardsView(View):

#     def get(self, request: HttpRequest):
#         card = Card.objects.get(number=request.GET['number'])

#         return JsonResponse({'card': {'number': card.number,
#                                       'expir_date': card.expir_date,
#                                       'cvv': card.cvv,
#                                       'date_of_issue': card.date_of_issue, 
#                                       'user_id': card.user_id,
#                                       'status': card.status}})


#     def post(self, request: HttpRequest):
#     	data = json.loads(request.body)
#     	card = Card(number=data['number'], expir_date=data['expir_date'], cvv=data['cvv'])
#     	card.save()

#     	return JsonResponse({'card': {'number': card.number,
#                                       'expir_date': card.expir_date,
#                                       'cvv': card.cvv,
#                                       'date_of_issue': card.date_of_issue, 
#                                       'user_id': card.user_id,
#                                       'status': card.status}})


def homeview(request):
    return render(request, 'cards/home.html', {'title': 'Home'})


def createview(request):
    if request.POST:
        try:
            data = request.POST
            card = Card(number=data['number'], expir_date=data['expir_date'], cvv=data['cvv'])
            card.save()
            check = False
        except:
            check = True
    else:
        check = False

    return render(request, 'cards/create.html', {'title': 'Create card',
                                                 'check': check})


def showview(request):
    if request.GET:
        card = Card.objects.filter(number=request.GET['number']).first()

    else:
        card = False

    return render(request, 'cards/show.html', {'title': 'Show card',
                                               'card': card})
