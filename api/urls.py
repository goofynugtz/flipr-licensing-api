from django.urls import path
from .views import *

urlpatterns = [
    path('issue/', issue, name='issue-key'),
    path('actions/validate', validate, name='validate-key'),
]
