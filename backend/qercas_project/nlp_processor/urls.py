from django.urls import path
from .views import RegulatorySearchView

urlpatterns = [
    path('search/', RegulatorySearchView.as_view(), name='regulatory-search'),
]

