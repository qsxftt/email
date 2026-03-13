from django.db import models
from django.contrib.auth.models import User

class Email(models.Model):
    FOLDER_CHOICES = (
        ('inbox', 'Входящие'),
        ('sent', 'Отправленные'),
        ('archive', 'Архив'),
        ('trash', 'Корзина'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    sender_email = models.CharField(max_length=255)
    recipient_email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    folder = models.CharField(max_length=10, choices=FOLDER_CHOICES, default='inbox')
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subject} - {self.recipient_email}'