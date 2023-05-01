from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (
    User, Profile, Divisions, Position, UserAccess, UserSession, ServerSettings
)


class UserRegisterSerializer(serializers.ModelSerializer):
    email_or_phone_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email_or_phone_number', 'surname', 'password')

    def validate_email_or_phone_number(self, value):
        if '@' in value:
            self.email = value.lower()
            self.phone_number = None
            if User.objects.filter(email=self.email).exists():
                raise ValidationError("Пользователь с такой электронной почтой уже зарегистрирован.")
        else:
            self.phone_number = value
            self.email = None
            if User.objects.filter(phone_number=self.phone_number).exists():
                raise ValidationError("Пользователь с таким номером телефона уже зарегистрирован.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=self.email,
            phone_number=self.phone_number,
            password=validated_data['password'],
            surname=validated_data['surname']
        )
        user.is_active = True
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_code(self, value):
        user = self.context['request'].user
        if value != user.reset_password_code:
            raise serializers.ValidationError('Неверный код подтверждения')
        return value

    def validate(self, data):
        password = data['password']
        user = self.context['request'].user
        user.set_password(password)
        user.reset_password_code = None
        user.save()
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'profile')


class DivisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisions
        fields = ('id', 'divisions')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'position')


class UserDataUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'surname', 'user')


class UserListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    profile = ProfileSerializer()
    divisions = DivisionsSerializer()
    position = PositionSerializer()

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'surname', 'profile', 'divisions', 'position', 'user', 'status', 'access')


class UserStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'surname', 'profile', 'divisions', 'position', 'email', 'phone_number', 'access')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'surname')


class ProfileGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'profile')


class UserAccessAllGetSerializer(serializers.ModelSerializer):
    user_profile = ProfileGetSerializer(source='user.profile', read_only=True)
    user = UserProfileSerializer()

    class Meta:
        model = UserAccess
        fields = "__all__"


class UserAccessUpdateSerializer(serializers.ModelSerializer):
    user_profile = ProfileGetSerializer(source='user.profile', read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserAccess
        fields = "__all__"


class UserSessionAllGetSerializer(serializers.ModelSerializer):
    user_profile = ProfileGetSerializer(source='user.profile', read_only=True)
    user = UserProfileSerializer()

    class Meta:
        model = UserSession
        fields = "__all__"


class UserSessionUpdateSerializer(serializers.ModelSerializer):
    user_profile = ProfileGetSerializer(source='user.profile', read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserSession
        fields = "__all__"


class ServerSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerSettings
        fields = ('id', 'session_timeout', 'server_url', 'server_password', 'dns', 'ip', 'https', 'ssl', 'status_server')
        read_only_fields = ('id',)

    def validate_server_url(self, value):
        if "http" not in value:
            raise serializers.ValidationError("Адрес сервера должен содержать 'http' или 'https'.")
        return value

    def validate_dns(self, value):
        if not value:
            raise serializers.ValidationError("Поле DNS не может быть пустым.")
        return value

    def validate_ip(self, value):
        if not value:
            raise serializers.ValidationError("Поле IP не может быть пустым.")
        return value

    def validate(self, data):
        if not data.get('dns') and not data.get('ip'):
            raise serializers.ValidationError("Должно быть заполнено хотя бы одно из полей DNS или IP.")
        return data


class SessionTimeoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerSettings
        fields = ('id', 'session_timeout')


class ServerSettingsUpdateSerializer(serializers.ModelSerializer):
    session_timeout = SessionTimeoutSerializer()

    class Meta:
        model = ServerSettings
        fields = ('id', 'session_timeout', 'server_url', 'server_password', 'dns', 'ip', 'https', 'ssl', 'status_server')
