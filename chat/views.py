from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import Room,Post,Answer
from django.contrib.auth import get_user_model
import json
import online_users.models
from datetime import timedelta
from itertools import chain
from user.models import CustomUser

User = get_user_model()

# Create your views here.
# @login_required
def index(request):
    if request.method=="POST":
        try:
            nq = request.POST.get('newqn')
            print(request.user.username)
            ins = Post(question = nq, created_by = request.user)
            ins.save()
        except Exception:
            post=request.POST.get('post')
            username=request.POST.get('username')
            answer=request.POST.get('answer')
            p=Post.objects.get(id=post)
            u=User.objects.get(username=username)

            ins=Answer(post=p,answer=answer,created_by=u)
            ins.save()
        return redirect('chat:index')
    else:
        posts = Post.objects.filter()
        answer = Answer.objects.filter()
        usernames=User.objects.only("username")
        rooms=Room.objects.order_by("created_at")
        available_rooms = Room.objects.filter()
        allusers=CustomUser.objects.all()

        #for online user list
        current = request.user
        on_users=[]
        user_status = online_users.models.OnlineUserActivity.objects.all()
        for user in user_status:
            a=user.user
            if a in allusers and a!= current:
                on_users.append(a) 
        print(on_users)
        return render(request,'chat/index.html',{"rooms":rooms,
            "usernames":usernames,"posts":posts,"answers":answer,"available_rooms":available_rooms, "onusers" : on_users})

# @login_required
def room(request, roomName, onuser):
    r_name = roomName
    o_id = onuser
    try:
        room=Room.objects.filter(members = onuser ).filter(members = request.user)[0]
        id=room.id
        rname = roomName
        allusers=CustomUser.objects.all()

        #for online user list
        on_users=[]
        user_status = online_users.models.OnlineUserActivity.objects.all()
        for user in user_status:
            a=user.user
            if a in allusers:
                on_users.append(a)     
        
        pass
    except IndexError:
        current_user = request.user
        memberlist = [onuser, request.user]
        ins=Room.objects.create()
        ins.members.set(memberlist)
        ins.save()
        room=Room.objects.filter(id=ins.id)[0]
        id=room.id
        allusers=CustomUser.objects.all()

          #for online user list
        on_users=[]
        user_status = online_users.models.OnlineUserActivity.objects.all()
        for user in user_status:
            a=user.user
            if a in allusers:
                on_users.append(a)
        pass
    return render(request,'chat/chatroom.html',{
        'room_name' : r_name,
        "o_id" : o_id,
        'username':mark_safe(json.dumps(request.user.username)),
        'id':id,'on_users':on_users,
        'allusers':allusers
    })


def delpost(request, postid):
    print(postid)
    ins = Post.objects.get(id = id)
    ins.delete()
    return redirect('chat:index')

def delans(request, ansid):
    print(ansid)
    ins = Answer.objects.get(id = id)
    ins.delete()
    return redirect('chat:index')