from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from config import exceptions as custom_exception
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers


# Set the default User Model here
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, providing methods to serialize and deserialize user instances. This serializer includes all fields 
    from the User model. Sets certain fields as read-only to ensure they cannot be modified through the serializer.
    Configures the 'password' field to be write-only for security reasons.
    Attributes: Meta (class): Contains configuration options for the serializer.
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_active', 'last_login',
        ]
        read_only_fields = ['username', 'email']
        extra_kwargs = {
            'password': { 'write_only': True }
        }

    def update(self, instance, validated_data):
        """
        Override the update method to handle custom update logic if needed. 
        :args: instance (User): validated_data (dict):
        :returns: user instance.
        """
        return super().update(instance, validated_data)


class SignUpSerializer(serializers.ModelSerializer):
    """
    This serializer is being called when any user want to register/sign-up. It will set the input type to password for security in forms.
    And ensure the password is not included in serialized output.
    """
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            'username',
            'email',
            'password',
        )

    password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True
        )

    def validate(self, attrs):
        """
        Custom validation logic for the password field. Create a User instance with the provided attributes.
        Get the password from the attributes.
        Finally, Validate the password using Django's built-in validators, If fails, capture the error messages
        :param: self, attributes
        :return: validated attributes
        """
        user = User(**attrs)
        password = attrs.get('password')
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            messages = [_(message) for message in e.messages]
            raise serializers.ValidationError({'password': messages})
        return attrs

    def create(self, validated_data):
        """
        Custom create method to handle user creation. Perform the actual creation of the user
        :param: self, attributes
        :return: newly created instance
        """
        try:
            validated_data['email'] = validated_data['email']
            validated_data['username'] = validated_data['username']
            validated_data['password'] = validated_data['password']
            user = self.perform_create(validated_data)
        except IntegrityError as e:
            raise custom_exception.AlreadyExists(
                _(f'Error: {e}'))
        return user

    @staticmethod
    def perform_create(validated_data):
        """
        Use a database transaction to ensure atomicity of the user creation.
        Create a new user with the validated data.
        :param: attributes
        :return: instance
        """
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = False
            user.save(update_fields=['is_active'])
        return user
    

class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for handling user login. It extends the TokenObtainPairSerializer to customize the validation process and modify the output.
    The primary functions of this serializer are to ensure that the password field is handled securely and is not included in the serialized output.
    To structure the response to include both tokens and user data.
    """
    def validate(self, validated_data):
        """
        Validate the login credentials and generate tokens. Also includes additional user data in the response.
        :returns: dict with `tokens` and `serialized user_data`
        """
        try:
            active_user = User.objects.get(username=validated_data['email'])
        except User.DoesNotExist:
            active_user = get_object_or_404(User, email=validated_data['email'])

        if not active_user.check_password(validated_data['password']):
            raise AuthenticationFailed("No User matches the given query.")
        if not active_user.is_active:
            raise AuthenticationFailed("Please verify your account first.")
        
        # Use the current user instance
        user = active_user
        
        data = super().validate(validated_data)
        data['token'] = {
            'refresh': data.pop('refresh'),
            'access': data.pop('access')
        }
        user_serializer = UserSerializer(user)
        data['user_data'] = user_serializer.data
        update_last_login(None, user)

        return data
    
