from django.urls import path

from chat.apps.main import views

urlpatterns = [
    path('health/', views.health, name='health'),

    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.log_out, name='logout'),
]
