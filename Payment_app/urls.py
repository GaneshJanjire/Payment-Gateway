from django.urls import path
from django.contrib import admin
from . import views
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("payment/", views.order_payment, name="payment"),
    path("callback/", views.callback, name="callback"),
    #path('callback/', CallbackView.as_view(), name='callback'), 
]

# from django.urls import path
# from .views import HomeView, OrderPaymentView, CallbackView

# urlpatterns = [
#     path('home/', HomeView.as_view(), name='home'),
#     path('order_payment/', OrderPaymentView.as_view(), name='order_payment'),
#     path('callback/', CallbackView.as_view(), name='callback'),
# ]



