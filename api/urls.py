from django.urls import path
from .views import *

urlpatterns = [
    path('issue/', issue, name='issue-key'),
    path('actions/validate/', validate, name='validate-key'),
    path('actions/suspend/', suspend, name='suspend'),
    path('actions/revoke/', revoke, name='revoke'),
    path('metrics/', compute_metrics, name='metrics')
]
