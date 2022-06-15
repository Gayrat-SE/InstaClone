from calendar import c
from multiprocessing import context
from pkgutil import ImpImporter
from django.shortcuts import render
from .models import Post, Tag, Follow, Stream
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    user= request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post.id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context = {'post_items': post_items}

    return render(request, 'index.html',context)