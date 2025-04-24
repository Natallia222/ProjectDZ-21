from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Post, Category
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from .forms import SubscriptionForm
from .models import Subscription
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


class CategoryPostListView(FormMixin, ListView):
    model = Post
    template_name = 'news/category_posts.html'
    context_object_name = 'posts'
    form_class = SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['category'] = category
        context['form'] = self.get_form()
        context['is_subscribed'] = False
        if self.request.user.is_authenticated:
            context['is_subscribed'] = Subscription.objects.filter(
                user=self.request.user,
                category=category
            ).exists()
        return context

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Post.objects.filter(category=category)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        category = Category.objects.get(pk=self.kwargs['pk'])
        Subscription.objects.get_or_create(user=request.user, category=category)
        return redirect(request.path)


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'


@method_decorator(login_required, name='dispatch')
def subscribe_to_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    user = request.user

    if not Subscription.objects.filter(user=user, category=category).exists():
        Subscription.objects.create(user=user, category=category)

    return redirect('category_posts', pk=pk)


@login_required
def subscribe_to_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.subscribers.add(request.user)
    messages.success(request, f'Вы подписались на категорию "{category.name}" 🎉')
    return redirect('category_posts', pk=pk)