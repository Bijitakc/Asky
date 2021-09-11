from django.db import models
from django.contrib.auth import get_user_model
import datetime


User=get_user_model()
# Create your models here.
class Post(models.Model):
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    answer = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)


class Room(models.Model):
    # answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=255)
    members = models.ManyToManyField(User,related_name="members")
    created_at=models.DateTimeField(auto_now_add=True)
    # created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    # access_users = models.ManyToManyField(User,related_name="access_users")
    #online_users=models.OneToOneField(User,on_delete=models.CASCADE, related_name='online',null=True) 
    #is_online=models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = "Rooms"

class Message(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    author=models.ForeignKey(User,related_name='author_messages',on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = "Messages"


    def __str__(self):
        return self.author.username




    #using this we can load last ten messages from the message model
    def last_10_messages(room):
        return Message.objects.filter(room=room).order_by('timestamp').all()[:10]



