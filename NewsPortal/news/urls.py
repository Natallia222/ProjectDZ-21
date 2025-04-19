from django.urls import path
from .views import CategoryPostListView, PostDetailView, subscribe_to_category


urlpatterns = [
    path('category/<int:pk>/', CategoryPostListView.as_view(), name='category_posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<int:pk>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]
