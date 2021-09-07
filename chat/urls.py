from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    # re_path(r'^(?P<room_name>[^/]+)/$',views.room, name='room'),
    path('<str:room_name>',views.room,name="room"),
    path('chatroomz/', views.chatroomz, name = "chatroomz")
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)