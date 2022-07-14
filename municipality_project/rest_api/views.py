from django.shortcuts import render

# Create your views here.
from rest_framework import generics as rest_views
from rest_framework import permissions

from municipality_project.rest_api.models import UserNotification
from municipality_project.rest_api.serializers import UserNotificationSerializer


class UserNotificationView(rest_views.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
