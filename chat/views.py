from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import Room,User,Post,Answer
import json
import online_users.models
from datetime import timedelta
from itertools import chain

# Create your views here.
@login_required
def index(request):
    posts = Post.objects.filter()
    answer = Answer.objects.filter()
    usernames=User.objects.only("username")
    rooms=Room.objects.order_by("created_at")
    available_rooms = Room.objects.filter()
    return render(request,'chat/index.html',{"rooms":rooms,
    "usernames":usernames,"posts":posts,"answers":answer,"available_rooms":available_rooms})

@login_required
def room(request,room_name):
    try:
        room=Room.objects.filter(title=room_name)[0]
        if not ( request.user in room.access_users.all() or request.user in User.objects.filter(groups__name='SMES')):
            return HttpResponse('You don\'t have permissions to access this room')
        
        id=room.id
        allusers=room.access_users.all()

        #for online user list
        on_users=[]
        user_status = online_users.models.OnlineUserActivity.objects.all()
        for user in user_status:
            a=user.user
            if a in allusers:
                on_users.append(a)     
        
        pass
    except IndexError:
        q = request.GET.get('q',None)
        answer = get_object_or_404(Answer,id=q)
        if Room.objects.filter(answer=answer).exists():
            room = Room.objects.get(answer=answer)
            return redirect(f"/chat/{room.title}")
        current_user = request.user
        ins=Room.objects.create(title=room_name,created_by=current_user,answer=answer)
        list_of_users = [answer.created_by,answer.post.created_by]
        for us in User.objects.filter(groups__name='SMES'):
            list_of_users.append(us)
        ins.access_users.set(list_of_users)
        ins.save()
        room=Room.objects.filter(title=room_name)[0]
        id=room.id
        allusers=room.access_users.all()

          #for online user list
        on_users=[]
        user_status = online_users.models.OnlineUserActivity.objects.all()
        for user in user_status:
            a=user.user
            if a in allusers:
                on_users.append(a)
        pass


    return render(request,'chat/chatroom.html',{
        'room_name':room_name,
        'username':mark_safe(json.dumps(request.user.username)),
        'id':id,'on_users':on_users,'allusers':allusers
    })
