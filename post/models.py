
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

# User files
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=250, verbose_name='Tag')
    slug = models.SlugField(max_length=50, unique=True, null=False, default=uuid.uuid1)


    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags',args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug - slugify(self.slug)
        return super().save(*args, **kwargs)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=True)
    caption = models.CharField(max_length=250, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post-details", args=[self.id])

    def __str__(self):
        return self.caption

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower.username + ' follows ' + self.following.username

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date = post.posted , following=user)
            stream.save()
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='likes_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_post')

    def __str__(self):
        return self.user.username + ' likes ' + self.post.caption



post_save.connect(Stream.add_post, sender=Post)