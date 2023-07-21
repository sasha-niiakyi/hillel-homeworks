from rest_framework import permissions
from .models import Card


class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.owner == request.user

