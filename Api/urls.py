from django.contrib import admin
from django.urls import path
from .views import MenuItemsView,MenuItemView,GroupsView,GroupView,DeliverysView,DeliveryView,CartsView,OrdersView,OrderView

urlpatterns = [
   path('menu-items/',MenuItemsView.as_view()),
   path('menu-items/<int:id>/',MenuItemView.as_view()),
   path('groups/manager/users/',GroupsView.as_view()),
   path('groups/manager/users/<int:id>/',GroupView.as_view()),
   path('groups/delivery-crew/users/',DeliverysView.as_view()),
   path('groups/delivery-crew/users/<int:id>',DeliveryView.as_view()),
   path('cart/menu-items/',CartsView.as_view()),
   path('orders/',OrdersView.as_view()),
   path('orders/<int:id>/',OrderView.as_view()),
]