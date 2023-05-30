
from rest_framework import serializers
from .models import Topic
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# This is a serializer class for the Topic model with fields including id, blog_title, blog_summary,
# blog_content, blog_header_image, and user_id.
class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model=Topic
        fields= ['id','blog_title','blog_summary','blog_content','blog_header_image','user_id','user']
        # depth = 1
        
     
 
# This is a serializer class for the User model with fields for id, first name, last name, and
# username.
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields= ['id','first_name','last_name','username']
        
        
# The class `MyTokenObtainPairSerializer` extends `TokenObtainPairSerializer` and adds a custom claim
# for the user's username to the token.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_email"] =self.user.email

        return data

    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token
    


    

# This is a serializer class for registering a user with fields such as email, password, first name,
# and last name.
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

# This is a class that defines the fields and extra keyword arguments for a User model in Django.
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


    def validate(self, attrs):
        """
        This function validates if the password and password2 fields match and raises a validation error if
        they don't.
        
        :param attrs: attrs is a dictionary containing the data submitted in the request. It is passed as an
        argument to the validate() method of a Django REST Framework serializer. The method is used to
        validate the data before it is saved to the database. In this case, the method checks if the
        password and password2 fields
        :return: The `attrs` dictionary is being returned after validating that the `password` and
        `password2` fields match.
        """

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

        
    def create(self, validated_data):
        """
        This function creates a new user object with the provided validated data and saves it to the
        database.
        
        :param validated_data: A dictionary containing the validated data for creating a new user. It
        includes the following keys:
        :return: The `create()` method returns the `user` object that was created and saved in the
        database.
        """
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        
        user.first_name = validated_data['first_name']
        user.last_name  = validated_data['last_name']
        user.save()
        return user