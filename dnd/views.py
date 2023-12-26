from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .forms import AdvUserForm, CharacterForm
from .serializers import AdvUserSerializer, CharacterSerializer
from .models import Character, AdvUser


def index(request):
    return render(request, 'layout/index.html')


class CreateUserView(APIView):
    def get(self, request):
        form = AdvUserForm()
        return render(request, 'profile/register.html', {'form': form})

    def post(self, request):
        serializer = AdvUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_activation_email(user, request)
            # Вместо простого возврата данных сериализатора, возвращаем дополнительное сообщение
            return Response({
                'user': serializer.data,
                'message': 'Регистрация прошла успешно. Письмо с подтверждением отправлено на вашу почту.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_activation_email(self, user, request):
        # Создание токена для пользователя
        token = token_generator.make_token(user)
        # Составление сообщения
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = request.get_host()
        subject = 'Активация вашего аккаунта на сайте DnD App'
        message = render_to_string('profile/activation_email.html', {
            'user': user,
            'domain': domain,
            'uid': uid,
            'token': token,
        })
        send_mail(
            subject,
            message,
            'davgo269@gmail.com',
            [user.email],
            fail_silently=False,
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return redirect('dnd:index')


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'profile/login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dnd:index')
        else:
            return render(request, 'profile/login.html', {'error': 'Неверные учетные данные.'})


@login_required
def user_profile(request):
    user = request.user
    characters = Character.objects.filter(user=user)
    return render(request, 'profile/profile.html', {'user': user, 'characters': characters})


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = AdvUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = AdvUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        characters = Character.objects.filter(user=user)
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()
            return redirect('profile')  # Предполагается, что у вас есть URL с именем 'profile'
    else:
        form = CharacterForm()
    return render(request, 'profile/create_character.html', {'form': form})
