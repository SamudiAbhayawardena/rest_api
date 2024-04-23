from .views import FoodRecomendationView, RecommendMealsView
from django.urls import path

urlpatterns = [
    path('get/', FoodRecomendationView.as_view(), name="foods"),
    path('get/meal/', RecommendMealsView.as_view(), name="meals")
]