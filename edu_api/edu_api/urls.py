"""edu_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve
from xadmin.plugins import xversion

xversion.register_models()

urlpatterns = [
    path('admin/', xadmin.site.urls),
    re_path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("home/", include("home.urls")),
    path("user/", include("user.urls")),
    path("course/", include("course.urls")),
    path("cart/", include("cart.urls")),
    path("order/", include("order.urls")),
]
