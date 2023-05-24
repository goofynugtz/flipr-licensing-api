from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
  path('signup/', first_signup, name='sign_up'),
  path('verify/<str:token>/', confirm_signup, name='sign_up_confirm'),
  path('forgot-password/', forgot_password_request, name='forgot_password'),
  path('reset-password/<str:token>/', reset_password, name='reset_password'),
  path('login/', CustomObtainPairView.as_view(), name='token_obtain_pair'),
  path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
