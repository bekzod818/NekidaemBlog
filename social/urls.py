from django.urls import path
from .views import BlogListView, BlogDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView, \
    PostDetailView, BlogFollowView, BlogUnfollowView, PostMarkAsReadView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name="post_edit"),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/mark_as_read/', PostMarkAsReadView.as_view(), name='post_mark_as_read'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/follow/', BlogFollowView.as_view(), name="follow"),
    path('<int:pk>/unfollow/', BlogUnfollowView.as_view(), name='unfollow'),
]
