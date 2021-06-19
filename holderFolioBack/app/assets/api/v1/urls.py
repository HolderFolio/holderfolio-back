from collections import namedtuple
from django.urls import path

from app.assets.api.v1.api import AssetCreateView, AssetRetrieveUpdateDestroyView, AssetListView

app_name = 'asset'

urlpatterns = [
    path('create/', AssetCreateView.as_view(), name='create_asset'),
    path('retrive/<int:pk>', AssetRetrieveUpdateDestroyView.as_view(), name='manage_asset'),
    path('list/', AssetListView.as_view(), name='list_asset')
]
