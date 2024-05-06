import random
import string

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import CustomUser
from user.tasks import send_forgot_password
from user.serializers import (
    RegistrationSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ConfirmForgotPasswordSerializer,
    AdminResetPasswordSerializer,
    )


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вам на почту было отправлено письмо с подтверждением вашей регистрации, пожалуйста перейдите по ссылке!', status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(CustomUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''.join(random.choice(string.ascii_letters + string.digits)for i in range(1,25))
        user.save(update_fields=['is_active', 'activation_code'])

        return Response('Вы успешно подтвердили регистрацию!', status=200)


class ChangePassword(APIView):
    serializer_class = ChangePasswordSerializer  

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data, context={'email': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'Успешно': 'Вы поменяли пароль'}, status=200)


class ForgotPassword(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = CustomUser.objects.get(email=request.data['email'])
        serializer = self.serializer_class(instance=request.data['email'], data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_forgot_password.delay(request.data['email'], email.activation_code)

        return Response('Мы отправили вам письмо на почту с ссылкой на сброс пароля!)')


class ConfirmForgotPassword(APIView):
    serializer_class = ConfirmForgotPasswordSerializer

    def put(self, request, pk):
        user = CustomUser.objects.get(activation_code=pk)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вы успешно сменили ваш пароль!)', status=status.HTTP_200_OK) # TODO


class AdminResetPassword(APIView):
    serializer_class = AdminResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response('Пароль пользователя успешно сменен и отправлен на почту)', status=status.HTTP_202_ACCEPTED)
