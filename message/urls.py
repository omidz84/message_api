from django.urls import path

from . import views

app_nam = 'message'
urlpatterns = [
    path('new/', views.CreateMessageView.as_view(), name='new-message'),
    path('send/group/', views.SendGroupMessageView.as_view(), name='send-group-message'),
    path('send/user/', views.SendUserMessageView.as_view(), name='send-group-message'),
    path('sent/list/', views.SentMessagesView.as_view(), name='sent-message'),
    path('received/list/', views.ReceivedMessagesView.as_view(), name='received-message'),
    path('reply/', views.ReplyMessageView.as_view(), name='reply-message'),
    path('reply/detail/<int:pk>/', views.DetailReplyMessageView.as_view(), name='detail-reply-message'),
    path('detail/<int:pk>/', views.DetailMessageView.as_view(), name='detail-message'),
    path('update/<int:pk>/', views.UpdateMessageView.as_view(), name='update-message'),
    path('unread/count/', views.UnreadMessagesCountView.as_view())
]
