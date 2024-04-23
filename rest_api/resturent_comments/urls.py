from django.urls import path, include
from .views import CommentHistorySetView, CommentHistoryGetView

urlpatterns = [
    path('set/', CommentHistorySetView.as_view(), name="comment add"),
    path('get/', CommentHistoryGetView.as_view(), name="comment get"),
]