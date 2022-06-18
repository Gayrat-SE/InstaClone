from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newpost/', views.newPost, name='newpost'),
    path('<uuid:post_id>/', views.PostDetail, name='postDetail'),
]
