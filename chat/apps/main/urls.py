from django.urls import path

from chat.apps.main import views

urlpatterns = [
    path('health/', views.health, name='health'),

    path('signup/', views.signup, name='signup'),
]
