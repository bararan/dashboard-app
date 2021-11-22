from django.urls import path
from .views import home_view, SalesListView, SaleDetailsView

app_name = 'sales'


urlpatterns = [
    path('', home_view, name='home'), #Leave the first argument an empty string for the main view.
    path('sales/', SalesListView.as_view(), name='list'),
    path('sales/<pk>', SaleDetailsView.as_view(), name='details'), # <pk> stands for primary key!
]