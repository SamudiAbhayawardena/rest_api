from django.urls import path, include
from .views import UserDetailsView, UserDetailsViewGet

urlpatterns = [
    path('data/', UserDetailsView.as_view(), name='user details'),
    path('data/get/', UserDetailsViewGet.as_view())
]
