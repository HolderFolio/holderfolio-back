from django.urls import path, include

from .api import (
    PortFolioCreateView, PortFolioRetriveUpdateView, PortFolioListView
)

app_name = 'portfolio'

urlpatterns = [
    path('create/', PortFolioCreateView.as_view() , name='create_portfolio'),
    path('list/', PortFolioListView.as_view() , name='list_portfolio'),
    path('retrive/<int:pk>/', PortFolioRetriveUpdateView.as_view() , name='get_portfolio'),
    path('update/<int:pk>/', PortFolioRetriveUpdateView.as_view() , name='update_portfolio'),
]

