from django.urls import path
from .views import ExplanationDetail, TransactionList, TransactionDetail, DashboardSummary

urlpatterns = [
    path('transactions/' , TransactionList.as_view(), name='transaction-list'),
    path('transactions/<uuid:pk>/', TransactionDetail.as_view(), name='transaction-detail'),
    path('transactions/<uuid:pk>/explanation/', ExplanationDetail.as_view() ,  name='expalanation-detail'),
     path('summary/', DashboardSummary.as_view(), name='dashboard-summary'),
]