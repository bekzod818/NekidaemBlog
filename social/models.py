from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import email_notification_subscriber


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    following = models.ManyToManyField(User, blank=True, related_name="following")
    user = models.ForeignKey(User, related_name="blog", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'

    def __str__(self):
        return self.title


class UsersReaderThrough(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    post = models.ForeignKey('social.Post', related_name='post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    users_read = models.ManyToManyField(User, related_name='user_read', through=UsersReaderThrough,
                                        through_fields=('post', 'user'), blank=True, verbose_name='Users have read')
    published = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, related_name="post", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        blog_title = instance.title
        post_url = 'http://0.0.0.0:8000/posts/%s' % instance.pk
        user_emails = instance.blog.following.values_list('email', flat=True)
        for email in user_emails:
            email_notification_subscriber.delay(email, blog_title, post_url)
