from django.urls import path

from municipality_project.rest_api.views import UserNotificationView

urlpatterns = [
    path('notification/', UserNotificationView.as_view(), name='notification')
]