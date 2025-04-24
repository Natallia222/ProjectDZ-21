import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Category


def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))

    subscribers_emails = set()
    for post in posts:
        subscribers = post.category.subscribers.all()
        subscribers_emails.update([user.email for user in subscribers if user.email])

    if subscribers_emails:
        send_mail(
            subject='Еженедельная рассылка свежих новостей 📰',
            message=f'Появились новые статьи в категориях: {", ".join(categories)}. Загляни на сайт!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(subscribers_emails),
            fail_silently=False,
        )
