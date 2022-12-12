from django.urls import path
from posts.views import *

urlpatterns = (
    path('posts/', PostView.as_view()),
    path('posts/<int:pk>/', DetailPostView.as_view()),
    path('posts/create/', post_create_view),
    path('hashtags/', HashtagsView.as_view()),
)
