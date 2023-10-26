from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.urls import  reverse
from django.http import  HttpResponse

UserModel = get_user_model()


def send_reset_password_emails(request):
    users = UserModel.objects.filter(is_active=True)  # отфильтровываем активных пользователей

    for user in users:
        if user.email:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

            subject = "Восстановление пароля"
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': uid,
                'token': token,
                'protocol': 'https' if request.is_secure() else 'http',
            })
            send_mail(subject, message, 'l_volkovskiy@bk.ru', [user.email], fail_silently=False)

    return HttpResponse(f"Письма успешно отправлены {len(users)} пользователям!")
