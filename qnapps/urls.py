"""qnapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import (login_view, logout_view, register_view)
from core.views import (superuser_index, superuser_qc)

urlpatterns = [
	path('admin/', admin.site.urls),
    
    path('superuser/<str:username>/', include([
        path('', superuser_index, name='superuser_index'),
        # path('question/<int:id>/answer/', views.new_answer, name='new_answer'),
        ])),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
	path('', include('core.urls', namespace='core')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
