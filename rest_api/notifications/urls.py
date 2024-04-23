from django.urls import path
from .views import NotificationsGetView, NotificationsSetView


urlpatterns = [
    path('get/', NotificationsGetView.as_view()),
    path('set/', NotificationsSetView.as_view()),
]