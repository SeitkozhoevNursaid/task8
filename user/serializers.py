import re
import random
import string

from django.utils import timezone
from django.contrib.auth.hashers import check_password

from rest_framework import serializers

from user.models import CustomUser, UserPasswords
from user.tasks import send_activation_code, send_reset_password


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
    )
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
    )
    password2 = serializers.CharField(
        max_length=128,
        write_only=True,
    )

    def validate(self, data):
        if not re.findall('\d', data['password']):
            raise serializers.ValidationError(
                ("В пароле обязательно должна быть 1 цифра"),
            )

        if not re.findall('[A-Z]', data['password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в верхнем регистре"),
            )

        if not re.findall('[a-z]', data['password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в нижнем регистре"),
            )

        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data['password']):
            raise serializers.ValidationError(
                ("В пароле должен быть 1 символ"),
            )

        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                ('Пароли не совпадают')
            )

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.setdefault('last_change_password', timezone.now())
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_code.delay(validated_data['email'], user.activation_code)
        
        UserPasswords.objects.create(password=user.password, user=user)
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        required=True,
        write_only=True,
        )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        )

    def validate(self, data):
        email = self.context['email']
        user = CustomUser.objects.get(email=email)  # TODO: related_name
        password_list = UserPasswords.objects.filter(user=user).order_by('-created_at')[:4]

        if not re.findall('\d', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно должна быть 1 цифра"),
            )

        if not re.findall('[A-Z]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в верхнем регистре"),
            )

        if not re.findall('[a-z]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в нижнем регистре"),
            )

        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле должен быть 1 символ"),
            )

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                ('Новые пароли не совпадают')
            )

        if data['password'] == data["new_password"]:
            raise serializers.ValidationError(
                ('Новый пароль не должен совпадать с текущим')
            )

        if not user.check_password(raw_password=data['password']):
            raise serializers.ValidationError(
                {'Ошибка': 'Пароль не сходится'}
            )

        if any(check_password(data["new_password"], prev_password.password) for prev_password in password_list):
            raise serializers.ValidationError(
                {'Ошибка': 'У вас уже был такой пароль'}
            )

        return data

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.last_change_password = timezone.now()
        instance.save(update_fields=['password', 'last_change_password'])

        UserPasswords.objects.create(password=instance.password, user=instance)
        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователя с такой почтой нет")
        return value

    def update(self, instance, validated_data):
        return instance


class ConfirmForgotPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if not re.findall('\d', data['new_password']):
             raise serializers.ValidationError(
                 ("В пароле обязательно должна быть 1 цифра"),
             )

        if not re.findall('[A-Z]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в верхнем регистре"),
            )

        if not re.findall('[a-z]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в нижнем регистре"),
            )

        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле должен быть 1 символ"),
            )

        if data['new_password'] != data['confirm_password']:
             raise serializers.ValidationError(
                 ('Новые пароли не совпадают')
             )

        return data

    def update(self, instance, validated_data):
        user = CustomUser.objects.get(email=instance)
        new_password = validated_data['new_password']
        user.set_password(new_password)
        user.last_change_password = timezone.now()
        user.save(update_fields=['password', 'last_change_password'])

        UserPasswords.objects.create(password=user.password, user=user)
        return instance


class AdminResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователя с такой почтой нет")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.get(email=validated_data['email'])
        new_password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(1,16))
        user.set_password(new_password)
        user.last_change_password = timezone.now()
        user.save(update_fields=['password', 'last_change_password'])
        send_reset_password.delay(validated_data['email'], new_password)

        UserPasswords.objects.create(password=user.password, user=user)
        return validated_data
