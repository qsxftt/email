from django.db import models


class MailUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Email(models.Model):
    owner = models.ForeignKey(MailUser, on_delete=models.CASCADE, related_name='owner_emails')
    sender = models.ForeignKey(MailUser, on_delete=models.CASCADE, related_name='sender_emails')
    recipient = models.ForeignKey(MailUser, on_delete=models.CASCADE, related_name='recipient_emails')
    topic = models.CharField(max_length=100)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    folder = models.CharField(max_length=100, default='inbox')

    def __str__(self):
        return self.topic
