"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import app.views
import authtest.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/<int:user_id>/', app.views.home, name='home'),
    path('home/Genre/<int:productcategory>/<int:user_id>/', app.views.home_Genre, name='home_Genre'),
    path('detail/<int:user_id>/<int:prod_id>/', app.views.detail, name='detail'),
    path('like/<int:user_id>/<int:prod_id>/', app.views.like, name='like'),
    path('payment/<int:user_id>/<int:prod_id>/', app.views.payment, name='payment'),
    path('sell/<int:user_id>/', app.views.sell, name='sell'),
    path('mypage/<int:user_id>/', app.views.mypage, name='mypage'),
    path('charge/<int:user_id>/', app.views.charge, name='charge'),
    path('login', authtest.views.login, name='login'),
    path('account/', authtest.views.account, name='account'),
    path('', app.views.home_notlogin, name = 'notlogin')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
