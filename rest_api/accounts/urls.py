from django.urls import path
from .views import RegisterUserView, LoginUserView, DeleteUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name="login"),
    path('delete/', DeleteUserView.as_view(), name="delete"),
]