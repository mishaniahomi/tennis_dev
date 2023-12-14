# -*- coding: utf-8 -*- 
from django.urls import path
from .views import index, registrations, code_control, CompetitionListView, CompetitionDetailView, OrderListApiView, \
    CreateRegistrationCompetition, OurLogoutView, privateOffice, OrderDeleteView, RegistrationCompetitionDeleteView, \
    check_free_table, OrderViewSet, GetPriceApiView

urlpatterns = [
    path('', index, name='main_index'),
    path('reg', registrations, name='registration'),
    path('check_free_table/', check_free_table, name='check_free_table'),
    path('api/get_orders/', OrderViewSet.as_view({'get': 'list'}), name='get_orders_api'),
    path('main_logout/', OurLogoutView.as_view(), name='main_logout'),
    path('privateOffice/', privateOffice, name='privateOffice'),
    path('privateOffice/order/delete/<int:pk>', OrderDeleteView.as_view(), name='OrderDeleteView'),
    path('privateOffice/RegistrationCompetitionDeleteView/delete/<int:pk>', RegistrationCompetitionDeleteView.as_view(), name='RegistrationCompetitionDeleteView'),
    path('code_control/<str:code>', code_control, name='code_control'),
    path('competitionlistview/', CompetitionListView.as_view(), name='competitionlistview'),
    path('competitionlistview/<int:pk>/', CompetitionDetailView.as_view(), name='competition_detail'),
    path('competitionlistview/<int:pk>/registration', CreateRegistrationCompetition, name='competition_registration'),
    path('api/order_list_view', OrderListApiView.as_view(), name="order_list_view"),
    path('api/get_price', GetPriceApiView.as_view(), name="order_list_view"),
]
