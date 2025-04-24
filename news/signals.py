from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscribers.all()
        emails = [user.email for user in subscribers if user.email]

        if emails:
            send_mail(
                subject=f"Новая публикация в категории: {category.name}",
                message=f"Привет! В категории '{category.name}' появилась новая статья: {instance.title}\n\n{instance.content[:200]}...",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=True,
            )