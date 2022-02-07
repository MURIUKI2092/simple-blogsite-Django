from django.urls import path
from . import views


urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerUser,name='register'),
    path('logout/',views.logoutUser,name="logout"),
    path('delete_chat/<str:primaryKey>',views.deleteChat,name="delete_chat"),
    path('profile/<str:primaryKey>',views.userProfile,name='user-profile'),
    path('',views.home,name="home"),
    path('room/<str:primaryKey>/',views.room,name='room'),
    path('create_room/',views.createRoom,name='create_room'),
    path('update_room/<str:primaryKey>',views.updateRoom,name='update_room'),
    path('delete_room/<str:primaryKey>',views.deleteRoom,name='delete_room'),
]