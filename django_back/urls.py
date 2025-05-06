"""
URL configuration for django_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import render
from django.urls import path, include, re_path
from django.views import View


class HomeView(View):

    def get(self, request):
        Response = render(request, 'index.html')
        # 5. 返回响应数据
        return Response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),
    path('api/data_manage/', include('data_manage.urls')),
    path('api/data_mark/', include('data_mark.urls')),
    path('api/data_mark/', include('data_label.urls')),

    path('api/statistics/', include('data_statistics.urls')),
    path('', HomeView.as_view()),
]

# 3. 通配路由（必须放在最后）
urlpatterns += [
    re_path(r'^(?!static/|media/|admin/|api/).*', HomeView.as_view()),
]

from django.conf import settings
from django.conf.urls.static import static

# 让 Django 开发服务器提供 `MEDIA_ROOT` 目录下的文件
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
