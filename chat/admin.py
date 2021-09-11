from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room,Message,Post,Answer

admin.site.register(Room)

admin.site.register(Message)

admin.site.register(Post)
admin.site.register(Answer)

