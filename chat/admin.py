from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room,Message,Post,Answer

admin.site.register(
    Room,
    list_display=["id", "title","created_at","created_by"],
    list_display_links=["id", "title"],
)

admin.site.register(
    Message,
    list_display=["room","author","content"],
    list_filter=["timestamp"]
)

admin.site.register(Post)
admin.site.register(Answer)

