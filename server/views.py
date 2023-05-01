from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from main.settings import EMAIL_HOST_USER, KEY_SMS
from .models import User, UserAccess, UserSession, ServerSettings
from .serializers import (UserRegisterSerializer, ResetPasswordSerializer, UserListSerializer,
                          UserStatusUpdateSerializer, UserDataUpdateSerializer, UserAccessAllGetSerializer,
                          UserAccessUpdateSerializer, UserSessionAllGetSerializer, UserSessionUpdateSerializer,
                          ServerSettingsSerializer, ServerSettingsUpdateSerializer)
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from requests.auth import HTTPProxyAuth
import requests


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'status': 201,
            'Сообщение': 'Пользователь успешно создан'
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UserAuthorization(APIView):
    def post(self, request):
        email_or_phone_number = request.data.get('email_or_phone_number')
        password = request.data.get('password')
        user = User.objects.filter(Q(email=email_or_phone_number) | Q(phone_number=email_or_phone_number)).first()
        if user is not None and user.is_active and user.check_password(password):
            if user.access:
                return Response({'Сообщение': 'У вас нет доступа к данному ресурсу'},
                                status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            return Response({'Сообщение': 'Вы успешно вошли в свой аккаунт!'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'Сообщение': 'Неверный email, номер телефона или пароль'},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response({'Сообщение': 'Вы успешно вышли из своего аккаунта.'}, status=status.HTTP_200_OK)


class UserSendingResetCode(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        email = user.email
        phone_number = user.phone_number
        code = str(random.randint(100000, 999999))
        user.reset_password_code = code
        user.save(update_fields=['reset_password_code'])
        if phone_number:
            url = f"https://sms.ru/code/call?phone={phone_number}&{KEY_SMS}{code}"
            response = requests.get(url)
            if response.status_code != 200:
                return Response({'Сообщение': 'Не удалось отправить SMS-код'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            subject = 'Код подтверждения для сброса пароля'
            message = f'Ваш код подтверждения: {code}'
            send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=False)
        return Response({'Сообщение': 'Код подтверждения отправлен'}, status=status.HTTP_200_OK)


class UserResetConfirmation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Сообщение': 'Пароль успешно сброшен'}, status=status.HTTP_200_OK)


class UserDataUpdate(generics.UpdateAPIView):
    serializer_class = UserDataUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Сообщение": "Профиль успешно обновлен", "data": serializer.data},
                        status=status.HTTP_200_OK)


class DataOutputUser(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)


class UserStatusUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['Сообщение'] = 'Пользователь успешно обновлен'
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['Сообщение'] = 'Пользователь успешно удален'
        return response


class UserAccessAllGet(generics.ListAPIView):
    queryset = UserAccess.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserAccessAllGetSerializer


class UserAccessUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccess.objects.all()
    serializer_class = UserAccessUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['Сообщение'] = 'успешно обновлен'
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['Сообщение'] = 'успешно удален'
        return response


class UserSessionAllGet(generics.ListAPIView):
    queryset = UserSession.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSessionAllGetSerializer


class UserSessionUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSession.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSessionUpdateSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['Сообщение'] = 'успешно обновлен'
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data['status'] = 200
        response.data['Сообщение'] = 'успешно удален'
        return response


class ServerSettingsGetCreate(generics.ListCreateAPIView):
    serializer_class = ServerSettingsSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return ServerSettings.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            ServerSettings.status_server = True
            serializer.save()
            return Response({"Сообщение": "Настройки сервера успешно созданы"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServerSettingsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServerSettingsSerializer
    queryset = ServerSettings.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({'message': 'Настройки сервера успешно удалены'}, status=status.HTTP_204_NO_CONTENT)
        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        status_server = serializer.validated_data.get('status_server', False)
        server_url = serializer.validated_data.get('server_url', None)
        server_password = serializer.validated_data.get('server_password', None)
        https = serializer.validated_data.get('https', None)
        dns = serializer.validated_data.get('dns', None)
        ip = serializer.validated_data.get('ip', None)
        ssl = serializer.validated_data.get('ssl', None)
        session_timeout = serializer.validated_data.get('session_timeout', None)
        if status_server:
            proxy = "http://yourproxyaddress.com:port"
            proxies = {"http": proxy, "https": proxy}
            auth = HTTPProxyAuth('username', 'password')
            session = requests.Session()
            session.proxies.update(proxies)
            session.auth = auth
        instance.save()
        return Response({'message': 'Настройки сервера успешно обновлены'}, status=status.HTTP_200_OK)
