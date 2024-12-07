from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from zeep import Client


from user import serializers
from user.models import OTPRequest, User


# Create your views here.

class SmsConsole:
    def __init__(self, username, password, to, text):
        self.username = username
        self.password = password
        self.to = to
        self.text = text

    def send_sms(self, bodyId):
        client = Client("https://api.payamak-panel.com/post/Send.asmx?wsdl")
        data = {
            "username": self.username,
            "password": self.password,
            "to": self.to,
            "text": self.text,
            "bodyId": bodyId
        }
        result = client.service.SendByBaseNumber(**data)
        return result


class OTPView(APIView):
    def get(self, request):
        serializer = serializers.RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPRequest.objects.generate(data)
                otp_code = OTPRequest.objects.filter(request_id=serializers.RequestOTPResponseSerializer(otp).data["request_id"]).first()
                melipayamak = SmsConsole("xx", "yy", to=str(otp_code.receiver), text=str(otp_code.password))
                melipayamak.send_sms(66337)
                return Response(data=serializers.RequestOTPResponseSerializer(otp).data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = serializers.VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(**data):
                return Response(data=self._handel_login(data), status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _handel_login(selfself, otp):
        User = get_user_model()
        query = User.objects.filter(username=otp['receiver'])
        if query.exists():
            created = False,
            user = query.first()
        else:
            created = True,
            user = User.objects.create(username=otp['receiver'])
        refresh_token = RefreshToken.for_user(user)

        return serializers.ObtainTokenSerializer({
            "refresh_token": str(refresh_token),
            "token": str(refresh_token.access_token),
            "created": created
        }).data
