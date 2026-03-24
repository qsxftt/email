from django.shortcuts import render, redirect
from .models import Email, MailUser

def current_user(request):
    user_id = request.session.get('user')
    if user_id:
        return MailUser.objects.get(id=user_id)
    else:
        return MailUser.objects.order_by('id').first()

def inbox(request):
    user = current_user(request)
    emails = Email.objects.filter(owner=user, folder='inbox')
    return render(request, 'emailbox/index.html', {'emails': emails, 'user': user, 'title': 'Входящие'})

def sent(request):
    user = current_user(request)
    emails = Email.objects.filter(owner=user, folder='sent')
    return render(request, 'emailbox/index.html', {'emails': emails, 'user': user, 'title': 'Отправленные'})

def archive(request):
    user = current_user(request)
    emails = Email.objects.filter(owner=user, folder='archive')
    return render(request, 'emailbox/index.html', {'emails': emails, 'user': user, 'title': 'Архив'})

def trash(request):
    user = current_user(request)
    emails = Email.objects.filter(owner=user, folder='trash')
    return render(request, 'emailbox/index.html', {'emails': emails, 'user': user, 'title': 'Корзина'})

def send_email(request):
    user = current_user(request)
    users = MailUser.objects.exclude(id=user.id)
    if request.method == 'GET':
        return render(request, 'emailbox/send_email.html', {'users': users, 'user': user})
    elif request.method == 'POST':
        topic = request.POST.get('topic')
        text = request.POST.get('text')
        recipient = MailUser.objects.get(id=request.POST.get('recipient'))

        Email.objects.create(
            topic=topic,
            text=text,
            owner=user,
            sender=user,
            recipient=recipient,
            folder='sent'
        )
        
        Email.objects.create(
            topic=topic,
            text=text,
            owner=recipient,
            sender=user,
            recipient=recipient,
            folder='inbox'
        )

        return redirect('inbox')
    
def detail_email(request, email_id):
    email = Email.objects.get(id=email_id)
    user = current_user(request)
    if request.method == 'GET':
        email.is_read = True
        email.save()
        if email.folder == 'trash' or email.folder == 'archive':
            status = True
        else:
            status = False

        return render(request, 'emailbox/detail_email.html', {'email': email, 'status': status})
    
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'archive':
            email.folder = 'archive'
            email.save()
        elif action == 'trash':
            email.folder = 'trash'
            email.save()
        elif action == 'delete':
            email.delete()
        elif action == 'return':
            if email.sender == user:
                email.folder = 'sent'
                email.save()
            else:
                email.folder = 'inbox'
                email.save()

        return redirect('inbox')

    
def select_user(request):
    if request.method == 'GET':
        users = MailUser.objects.all()
        return render(request, 'emailbox/select_user.html', {'users': users})
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        request.session['user'] = user_id
        return redirect('inbox')