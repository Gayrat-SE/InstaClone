from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newpost/', views.newPost, name='newpost'),
    path('<uuid:post_id>/', views.PostDetail, name='post-details'),
    path('tags/<slug:tag_slug>/', views.tags, name='tags'),
    path('<uuid:post_id>/like/', views.like, name='like'),
]
