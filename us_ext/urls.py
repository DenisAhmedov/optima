from django.urls import path

from us_ext.views.contracts_views import ContractsView, ContractView

urlpatterns = [
    path('contracts/', ContractsView.as_view(), name='contracts'),
    path('contracts/<str:contract_number>/', ContractView.as_view(), name='contract'),

]
