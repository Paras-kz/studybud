from django.urls import URLPattern, path
from . import views
urlpatterns=[
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('',views.home,name='home'),
    #if path is ->  ' ' then go to views.home fn.
    path('room/<str:k>/',views.room,name='room'),
    path('profile/<str:pk>/',views.userProfile,name="user-Profile"),#1 from here go to views.userProfile
    path('create-room',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message')
]