from django.urls import path,include
from .views import signup,loginpage,logoutpage

urlpatterns = [
    path('signup/',signup,name="signup"),
    path('login/',loginpage,name="loginpage"),
    path('logout/',logoutpage,name="logoutpage")
]
