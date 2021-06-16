from django.urls import path

from .api import (
    ExchangeCreateView, ExchangeRetrieveUpdateDestroyView, ExchangeListView
)

app_name = 'exchange'

urlpatterns = [
    path('create/', ExchangeCreateView.as_view(), name='create_exchange'),
    path('manage/<int:pk>/', ExchangeRetrieveUpdateDestroyView.as_view(),
         name='manage_exchange'),
    path('list/', ExchangeListView.as_view(), name='list_exchange')
]
