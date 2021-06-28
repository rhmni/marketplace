from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app_account.models import User


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    name = serializers.CharField()
    password = serializers.CharField()

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError('phone must be 11 character')
        if not value.isnumeric():
            raise serializers.ValidationError('phone must be only number')
        if not value.startswith('09'):
            raise serializers.ValidationError('phone must start with "09"')
        return value

    def validate_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password


class UserVerificationSerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate_code(self, value):
        if len(str(value)) != 6:
            raise serializers.ValidationError('code must be 6 character')
        return value


class UserForgetSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError('phone must be 11 character')
        if not value.isnumeric():
            raise serializers.ValidationError('phone must be only number')
        if not value.startswith('09'):
            raise serializers.ValidationError('phone must start with "09"')
        return value


class UserVerificationPasswordSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    password = serializers.CharField()

    def validate_code(self, value):
        if len(str(value)) != 6:
            raise serializers.ValidationError('code must be 6 character')
        return value

    def validate_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=70)
    new_password = serializers.CharField(max_length=70)

    def validate_new_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password

    def validate_old_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password


class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'name',
            'last_update',
        )

        read_only_fields = (
            'last_update',
        )
