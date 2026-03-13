from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Email
from django.utils import timezone

@login_required
def inbox(req):
    emls = Email.objects.filter(user=req.user, folder='inbox').order_by('-sent_at')
    return render(req, 'email_app/inbox.html', {'emails': emls, 'folder': 'inbox'})

@login_required
def sent(req):
    emls = Email.objects.filter(user=req.user, folder='sent').order_by('-sent_at')
    return render(req, 'email_app/inbox.html', {'emails': emls, 'folder': 'sent'})

@login_required
def archive(req):
    emls = Email.objects.filter(user=req.user, folder='archive').order_by('-sent_at')
    return render(req, 'email_app/inbox.html', {'emails': emls, 'folder': 'archive'})

@login_required
def trash(req):
    emls = Email.objects.filter(user=req.user, folder='trash').order_by('-sent_at')
    return render(req, 'email_app/inbox.html', {'emails': emls, 'folder': 'trash'})

@login_required
def detail(req, pk):
    em = get_object_or_404(Email, pk=pk, user=req.user)
    if not em.is_read and em.folder == 'inbox':
        em.is_read = True
        em.save()
    return render(req, 'email_app/detail.html', {'email': em})

@login_required
def compose(req):
    if req.method == 'POST':
        recipient_username = req.POST.get('recipient')
        subject = req.POST.get('subject')
        body = req.POST.get('body')
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            users = User.objects.exclude(username=req.user.username)
            return render(req, 'email_app/compose.html', {
                'error': 'Пользователь не существует',
                'users': users
            })
        Email.objects.create(
            user=req.user,
            sender_email=req.user.email or req.user.username,
            recipient_email=recipient.email or recipient.username,
            subject=subject,
            body=body,
            folder='sent',
            is_read=True
        )
        Email.objects.create(
            user=recipient,
            sender_email=req.user.email or req.user.username,
            recipient_email=recipient.email or recipient.username,
            subject=subject,
            body=body,
            folder='inbox',
            is_read=False
        )
        return redirect('sent')
    else:
        users = User.objects.exclude(username=req.user.username)
        return render(req, 'email_app/compose.html', {'users': users})
    
@login_required
def move(req, pk):
    if req.method == 'POST':
        em = get_object_or_404(Email, pk=pk, user=req.user)
        new_folder = req.POST.get('folder')
        if new_folder in dict(Email.FOLDER_CHOICES).keys():
            em.folder = new_folder
            em.save()
    return redirect(req.META.get('HTTP_REFERER', 'inbox'))

@login_required
def delete_permanent(req, pk):
    em = get_object_or_404(Email, pk=pk, user=req.user, folder='trash')
    em.delete()
    return redirect('trash')