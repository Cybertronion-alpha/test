from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message
from chat.serializers import MessageSerializer, UserSerializer
from django.contrib.auth.decorators import login_required

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@login_required
def chat_view(request):
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})

@login_required
def message_view(request, sender, receiver):
    if request.method=="POST":
        if sender!=receiver:
            return render(request, "chat/messages.html",
                        {'users': User.objects.exclude(username=request.user.username),
                        'receiver': User.objects.get(id=receiver),
                        'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                    Message.objects.filter(sender_id=receiver, receiver_id=sender)})
