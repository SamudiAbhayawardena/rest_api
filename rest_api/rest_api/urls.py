from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/user-details/', include('user_details.urls')),
    path('api/history/', include('health_history.urls')),
    path('api/foods/', include('food_recomendation.urls')),
    path('api/resturents/', include('resturent_recomendation.urls')),
    path('api/comment/', include('resturent_comments.urls')),
    path('api/notifications/', include('notifications.urls')),
]
