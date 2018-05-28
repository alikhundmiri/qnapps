"""dlauncher URL Configuration

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

from django.urls import path, include
from . import views

app_name = 'core'
urlpatterns = [
    path('', include([
        path('', views.index, name='home'),
        path('new/', views.browse_new, name='browse_new'),
        path('trend/', views.browse_trend, name='browse_trend'),
        path('favourite/', views.browse_favourite, name='browse_favourite'),
        ])),
    path('lander/', views.lander , name='lander'),

    # Links to enter new question and answers
    path('<str:username>/new/', include([
        path('question/', views.new_question, name='new_question'),
        path('question/<int:id>/answer/', views.new_answer, name='new_answer'),
        ])),

    # Links to view existing links
    path('question/<int:id>', views.question_detail, name='question_detail'),
    ]