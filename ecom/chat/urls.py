from django.urls import path
from . import views


urlpatterns = [
    #path('', views.index, name='index'),
    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages', views.message_list, name='message-list'),

    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    
    #path('api/users/<int:pk>', views.user_list, name='user-detail'),
    #path('api/users', views.user_list, name='user-list'),
]