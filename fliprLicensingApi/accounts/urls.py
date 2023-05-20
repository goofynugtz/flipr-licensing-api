from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
  path('signup/', signup, name='sign_up'),
  path('forgot-password/', forgot_password_request, name='forgot_password'),
  path('reset-password/<str:token>/', reset_password, name='reset_password'),
  path('login/', CustomObtainPairView.as_view(), name='token_obtain_pair'),
  path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
