from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Blog, Post, UsersReaderThrough
from django.urls import reverse_lazy
from django.http import JsonResponse


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    queryset = Blog.objects.all()
    template_name = 'blog_list.html'
    # paginate_by = 5


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'posts'
    slug_url_kwarg = 'slug'
    template_name = 'blog_detail.html'

    # paginate_by = 5

    def get_object(self, queryset=None):
        super(BlogDetailView, self).get_object(queryset)
        return Post.objects.filter(blog__slug=self.kwargs['slug'])


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'

    # paginate_by = 5

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return Post.objects.filter(blog__following__in=[self.request.user]).order_by('-id')
        return []


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'description', 'blog']
    success_url = reverse_lazy('post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'description', 'blog']
    success_url = reverse_lazy('post_list')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    template_name = 'post_detail.html'


class BlogFollowView(CreateView):
    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs.get('pk'))
        user = request.user
        if not blog.following.filter(pk=user.pk).exists():
            blog.following.add(user)
            return JsonResponse({'message': f'User {user} following.'})
        return JsonResponse({'message': f'User {user} already following.'})


class BlogUnfollowView(CreateView):
    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs.get('pk'))
        user = request.user
        if blog.following.filter(pk=user.pk).exists():
            blog.following.remove(user)
            readers = blog.post.values_list('users_read', flat=True)
            UsersReaderThrough.objects.filter(user__in=readers).delete()
            return JsonResponse({'message': f'User {user} unfollowing.'})
        return JsonResponse({'message': f'User {user} already unfollowing.'})


class PostMarkAsReadView(CreateView):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        user = request.user
        if not post.users_read.filter(pk=user.pk).exists():
            post.users_read.add(user)
            return JsonResponse({'message': f'Post has marked as read for user {user}'})
        return JsonResponse({'message': f'User {user} has already canceled this post as read'})
