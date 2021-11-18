from django.urls import path

from .views import RegistrationView, UserProfileView, CustomAuthToken


urlpatterns = [
    path('registration', RegistrationView.as_view()),
    path('api-token-auth', CustomAuthToken.as_view()),
    path('authentication', UserProfileView.as_view())
]
