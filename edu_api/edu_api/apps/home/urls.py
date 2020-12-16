from django.urls import path
from home import views

urlpatterns = [
    path("banners/", views.BannerAPIView.as_view()),
    path("up_nav/", views.NavAPIView.as_view()),
    path("down_nav/", views.NavsAPIView.as_view())

]
