# app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('account/create', AccountView.as_view(), name='account_create'),
    path('account/', AccountView.as_view(), name='account'),
    path('account/transaction', TransactionView.as_view(), name='transaction'),
    path('account/analytics', AnalyticsDataView.as_view(), name='analytics'),
]
