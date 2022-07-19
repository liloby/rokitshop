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
    path('profile/<int:pk>/delete/', views.ItemDelete.as_view(), name='unlisted_delete'),
    path('profile/<int:pk>/update/', views.ItemUpdate.as_view(), name='unlisted_update'),
    path('profile/<int:item_id>/add_post/', views.add_post, name='add_post'),
       # path('detail/<int:pk>/create/', views.BidCreate.as_view(), name='create_bid'),
    path('items/<int:item_id/add_bid/', views.add_bid, name='add_bid'),
   ]