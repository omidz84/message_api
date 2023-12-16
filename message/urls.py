from django.urls import path

from . import views

app_nam = 'message'
urlpatterns = [
    path('new/', views.CreateMessageView.as_view(), name='new-message'),
    path('send/group/', views.SendGroupMessageView.as_view(), name='send-group-message'),
    path('send/user/', views.SendUserMessageView.as_view(), name='send-user-message'),
    path('sent/list/', views.SentMessagesView.as_view(), name='sent-message'),
    path('received/list/', views.ReceivedMessagesView.as_view(), name='received-message'),
    path('detail/<int:pk>/', views.DetailMessageView.as_view(), name='detail-message'),
    path('unread/count/', views.UnreadMessagesCountView.as_view(), name='unread-message'),
    path('reply/', views.ReplyMessageView.as_view(), name='reply-message'),
    path('reply/<int:parent>/', views.ShowReplyMessageView.as_view(), name='show-reply-message'),
    path('delete/<int:pk>/', views.DeleteMessageView.as_view(), name='delete-message'),
]
