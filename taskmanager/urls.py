from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_index, name='api_index'),
    path('all/', views.api_all_tasks, name='api_all_tasks'),
    path('new/', views.api_new_task, name='api_new_task'),
    path('update/', views.api_update_task, name='api_update_task'),
    path('delete/', views.api_delete_task, name='api_delete_task'),
    path('signin/', views.api_signin, name='api_signin'),

    path('signup/', views.api_signup, name='api_signup'),
    path('loginByUsername/', views.loginByUsername, name='loginByUsername'),
    path('getServices/', views.getServices, name='getServices'),
    path('createBooking/', views.createBooking, name='createBooking'),
    path('getBooking/', views.getBooking, name='getBooking'),
]
