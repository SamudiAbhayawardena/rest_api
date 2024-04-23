from django.urls import path
from .views import ResturentRecomendationView

urlpatterns = [
    path('get/', ResturentRecomendationView.as_view()),
]