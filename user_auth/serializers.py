from rest_framework import serializers
from .models import userRegister
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .utils import send_email_verification

User = get_user_model()

class RegistrationsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required=True)
    password2 = serializers.CharField(write_only = True,required = True)

    #this function checks the validation in between the two attributes of the userRegister model 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    class Meta:
        model = userRegister
        fields = ['firstName','lastName','email','phone','password','password2'] #when address is needed add it here
    
    def create(self,validated_data):
        password = validated_data.pop('password',None)#the validated data is popped & store in the variable
        password2 = validated_data.pop('password2',None)
        phone = validated_data.pop('phone',None)
        #add address parameter below and pop that validated data and store it in address
        user = User.objects.create(
            username = validated_data['email'],
            first_name = validated_data.get('firstName'),
            last_name = validated_data.get('lastName'),
            email = validated_data['email'],
            )
        # if password != password2: this stopped from inputting data in userRegister table but not auth_user
        #      raise serializers.ValidationError("Passwords do not match")
        if password is not None and password == password2:
            user.set_password(password)
            user.is_active = False
            user.save()
        user_register = userRegister.objects.create(user=user,**validated_data,phone = phone)
        return user_register


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email','password']
    # email = serializers.EmailField()
    # password = serializers.CharField()
        
    
class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only = True, required=True)
    confirm_new_password = serializers.CharField(write_only = True, required=True)

    # def validate(self, attrs):
    #     if attrs['new_password'] != attrs['confirm_new_password']:
    #         raise serializers.ValidationError("Passwords do not match.")
    #     return attrs
    
    class Meta:
        model = User
        fields = ['new_password','confirm_new_password']
