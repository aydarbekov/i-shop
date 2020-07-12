from django.urls import path
from .views import OrderView
app_name = "api"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('orders/', OrderView.as_view()),
]