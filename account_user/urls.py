from django.urls import path

from .views import RegistrationView, AuthenticationView, CustomAuthToken


urlpatterns = [
    path('users', RegistrationView.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('authentication/', AuthenticationView.as_view())
]
