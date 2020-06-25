from django.contrib import admin
from django.urls import path
from recommend import views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index)


]
