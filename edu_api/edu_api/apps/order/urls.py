from django.urls import path
from order import views

urlpatterns = [
    path("orders/", views.OrderAPIView.as_view()),
]
