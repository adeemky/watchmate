from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('watch/', include('watchlist_app.api.urls')),
    path('auth/', include('user_app.api.urls')),
]
  