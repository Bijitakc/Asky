from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('chat.urls','chat'),namespace="chat")),
    path('user/',include(('user.urls',"user"),namespace="user"))
]

