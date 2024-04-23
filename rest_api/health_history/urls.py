from django.urls import path, include
from .views import HistoryView, HistoryViewGet

urlpatterns = [
    path('add/', HistoryView.as_view(), name="history add"),
    path('get/', HistoryViewGet.as_view(), name="history get")
]