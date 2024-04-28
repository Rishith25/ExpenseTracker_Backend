# app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('account/create', AccountView.as_view(), name='account_create'),
    path('account/', AccountView.as_view(), name='account'),
    path('account/<int:pk>/', AccountView.as_view(), name='account update'),
    path('account/transaction', TransactionView.as_view(), name='transaction'),
    path('account/transaction/<int:pk>', TransactionView.as_view(), name='update and delete'),
    path('account/analytics', AnalyticsDataView.as_view(), name='analytics'),
]
