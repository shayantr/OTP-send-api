from rest_framework import serializers

from user.models import OTPRequest


class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=True)
    channel = serializers.ChoiceField(allow_null=False, choices=OTPRequest.OtpChannel.choices)


class RequestOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ('request_id', )


class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.CharField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)


class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh_token = serializers.CharField(max_length=128, allow_null=False)
    created = serializers.BooleanField()