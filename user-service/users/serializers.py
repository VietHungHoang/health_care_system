from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, UserSession


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'role',
            'date_of_birth', 'gender', 'address'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth', 'gender', 'address',
            'emergency_contact', 'role', 'is_verified', 'profile_image',
            'created_at', 'updated_at', 'last_login'
        )
        read_only_fields = ('id', 'email', 'role', 'is_verified', 'created_at', 'updated_at')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for user profile including extended profile
    """
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'date_of_birth', 'gender', 'address',
            'emergency_contact', 'role', 'is_verified', 'profile_image',
            'created_at', 'updated_at', 'last_login', 'profile'
        )
        read_only_fields = ('id', 'email', 'role', 'is_verified', 'created_at', 'updated_at')
    
    def get_profile(self, obj):
        try:
            profile = obj.profile
            return ExtendedUserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None


class ExtendedUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for extended user profile
    """
    class Meta:
        model = UserProfile
        fields = (
            'bio', 'website', 'location', 'birth_place',
            'blood_type', 'allergies', 'medical_history', 'current_medications',
            'license_number', 'specialization', 'years_of_experience',
            'education', 'certifications', 'profile_visibility'
        )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class UserSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for user sessions
    """
    class Meta:
        model = UserSession
        fields = (
            'id', 'session_key', 'ip_address', 'user_agent',
            'device_info', 'location', 'is_active',
            'created_at', 'last_activity'
        )
        read_only_fields = ('id', 'created_at', 'last_activity')


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users (admin only)
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'full_name', 'role',
            'is_active', 'is_verified', 'created_at', 'last_login'
        )
        read_only_fields = fields