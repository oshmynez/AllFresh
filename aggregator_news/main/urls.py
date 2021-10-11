from django.urls import path
from . import views

urlpatterns = [
    path('search/<int:page_id>/', views.search),
    path('', views.main, name='index'),
    path('<str:topic>/<int:page_id>/', views.main),

]
