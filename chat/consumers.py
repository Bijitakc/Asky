from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message,Room

class ChatRoomConsumer(WebsocketConsumer):

    #recieve the messages
    def fetch_messages(self,data):
        id=data['roomid']
        try:
            room=Room.objects.filter(id=id)[0]
            messages=Message.last_10_messages(room)
            content={
                'command':'messages',
                'messages':self.messages_to_json(messages)
            }
            self.send_message(content)
            pass
        except IndexError:
            pass


    def new_message(self,data):
        User = get_user_model()
        author=data['from']
        author=author.replace('"','')
        author_user=User.objects.get(username=author)
        roomid=data['roomid']
        room=Room.objects.get(id=roomid)
        message=Message.objects.create(
            room=room,
            author=author_user,
            content=data['message'])
        content={
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        return self.send_chat_message(content)


    #change them into JSON for a storable format ie serializing
    def messages_to_json(self,messages):
        result=[]
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def message_to_json(self,message):
        return{
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.timestamp)
        }

    commands={
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }

    def connect(self):
        #allows to select room name by itself
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name
        
       
       #Used to join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept() 
       
    def disconnect(self,close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self,text_data):
        data=json.loads(text_data)
        self.commands[data['command']](self,data)


    def send_chat_message(self,message):

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chatroom_message',
                'message':message,
            }
        )

    def send_message(self,message):
        self.send(text_data=json.dumps(message))

    def chatroom_message(self,event):
        message=event['message']
        self.send(text_data=json.dumps(message))


