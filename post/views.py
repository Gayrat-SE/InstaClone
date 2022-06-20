
from multiprocessing import context
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from .models import Post, Tag, Follow, Stream, Likes
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponseRedirect
from .forms import  NewPostform
# Create your views here.
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField

def index(request):
    user= request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post.id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context = {'post_items': post_items}
    
    return render(request, 'index.html',context)




def newPost(request):
    user = request.user
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tag.set(tags_obj)
            p.save()
            print("hello")
            return redirect('index')
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)            


def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'details.html', context)

def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tag=tag).order_by('-posted')
    context = {'posts': posts, 'tag': tag}
    
    return render(request, 'tag.html', context)


def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes += 1
    else:
        liked = Likes.objects.get(user=user, post=post).delete()
        current_likes -= 1

    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))
