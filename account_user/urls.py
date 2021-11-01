from django.urls import path

from .views import RegisterView, AuthenticationView, CustomAuthToken


urlpatterns = [
    path('users', RegisterView.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('authentication/', AuthenticationView.as_view())
]
