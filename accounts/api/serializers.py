from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date,datetime
from utils.validators import is_validate_birth_date,is_validate_password
from accounts.models import Password_Token
User = get_user_model()

class UserSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(required = True)
    password2 = serializers.CharField(write_only = True, required = True)
    class Meta:
        model = User
        avatar = serializers.FileField(required = False)
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'birth_date',
            'password',
            'password2'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password do not match."})
        validated_password = is_validate_password(attrs['password'])

        if isinstance(validated_password,list):
            raise serializers.ValidationError(validated_password[0])
        return attrs
    
    def validate_birth_date(self,value):
        validated_birth_date = is_validate_birth_date(value)
        if validated_birth_date:
            raise serializers.ValidationError("your age must be at least 18+.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data.get('first_name',''),
            last_name = validated_data.get('last_name',''),
            avatar = validated_data.get('avatar',''),
            birth_date = validated_data['birth_date'],
            password = validated_data['password']
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username','email','first_name','last_name','avatar','birth_date'
        )
    
    def validate_birth_date(self, value):
        validated_birth_date = is_validate_birth_date(value)
        if validated_birth_date:    
            raise serializers.ValidationError("You must be at least 18+.")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

    def validate_password(self, value):
        validated_password = is_validate_password(value)
        if isinstance(validated_password,list):
            raise serializers.ValidationError(validated_password[0])
        return value

class CheckEmailExistsSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email = value)
            Password_Token.objects.get_or_create(user = user)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("This email does not exists.")

class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required = True)
    password2 = serializers.CharField(required = True)

    def validate(self, attrs):
        password1 = attrs['password1']
        password2 = attrs['password2']

        if password1 != password2:
            raise serializers.ValidationError("The password did not match.")
        
        validated_password = is_validate_password(password1)
        if isinstance(validated_password,list):
            raise serializers.ValidationError(validated_password[0])
        
        return attrs