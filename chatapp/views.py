from django.contrib.auth.models import User              # Django Build in User Model
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message                                 # Our Message model
from .serializers import MessageSerializer, UserSerializer
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
# Users View
@csrf_exempt                         # Decorator to make the view csrf excempt.
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:                 # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)        # Select only that particular user
        else:
            users = User.objects.all()                    # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request}) 
        return JsonResponse(serializer.data, safe=False)    # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)  # On POST, parse the request object to obtain the data in json
        serializer = UserSerializer(data=data)     # Seraialize the data
        if serializer.is_valid():
            serializer.save()                                   # Save it if valid
            return JsonResponse(serializer.data, status=201)     # Return back the data on success
        return JsonResponse(serializer.errors, status=400)     # Return back the errors  if not valid

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

    def get(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).get(request, format=None)

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = "chat_consumer"
        self.room_group_name = "chat_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.room_group_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status' : 'connected from dj channel'}))

    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status' : 'we got you'}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)