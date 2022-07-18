from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('items/create/', views.ItemCreate.as_view(), name='items_create'),
    path('items/', views.items_index, name='index'),
    path('items/<int:item_id>/', views.items_detail, name='detail'),
]