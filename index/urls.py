from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name="index"),
     path('logout', views.logout_view, name="logout"),
     path('login', views.login_view, name="login"),
     path('register', views.register, name="register"),
     path('create', views.sell_item, name="sell_item"),
     path('i/<int:id>', views.item, name="item"),
     path('i/<int:id>/edit', views.edit_item, name="edit_item"),
     path('i/<int:id>/delete', views.delete_item, name="delete_item"),
     path('like', views.like, name="like"),
     path('unlike', views.unlike, name="unlike"),
     path('404', views.FourZeroFour, name="404")
]
