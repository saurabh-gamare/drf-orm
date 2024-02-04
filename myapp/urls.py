from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.orm, name='orm'),
    path('index', views.orm2, name='orm2'),
]
