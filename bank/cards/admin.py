from django.contrib import admin
from .models import Card, Status


class CardAdmin(admin.ModelAdmin):
	list_display = ('number', 'date_of_issue', 'expir_date', 'status')
	list_filter = ('date_of_issue', 'expir_date', 'status')


admin.site.register(Card, CardAdmin)
admin.site.register(Status)