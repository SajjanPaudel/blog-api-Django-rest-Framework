from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics,mixins
from .serializers import TopicSerializer,UserSerializer
from .models import Topic
from functools import wraps 
import json
from .permissions import IsOwnerOrReadOnly
from rest_framework.parsers import JSONParser
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import MyTokenObtainPairSerializer,RegisterSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter



# This is a custom view class that extends TokenObtainPairView and allows any user to obtain a token
# pair using MyTokenObtainPairSerializer.

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
# This is a Django REST framework view for registering new users with the specified serializer and
# permission classes.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

def is_author(view_func):
    """
    This is a Python function that checks if the user requesting a function is the author of a blog post
    and returns an access forbidden error if not.
    
    :param view_func: a function that takes a request object and returns an HTTP response
    :return: The function `wrapper` is being returned as a decorator.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        blog_id = kwargs.get('id')
        blog = get_object_or_404(Topic, id=blog_id)
        #check if the author and the user who is requesting a function is same or not
        if request.user != blog.user:
        #if not then give an access forbidden error 
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return wrapper



"""
    This function returns a dictionary of API endpoints for a version 1 API.
    
    :param request: The request object represents the current HTTP request that is being made
    :return: The function `api_home` returns a response containing a dictionary of API endpoints with
    their corresponding URLs.
    """
@api_view(['GET'])
def api_home(request):
    api_urls={
        'List':'api/v1/list/',
        'Detail View':'api/v1/detail/<int:id>',
        'Create':'api/v1/create',
        'Update':'api/v1/update/<int:id>',
        'Delete':'api/v1/delete/<int:id>',
        'Get Token':'api/v1/gettoken',
        'Get Token':'api/v1/refreshtoken',
        'login':'/api-auth/login/'
    }
    
    return Response(api_urls)



# This is a Django REST framework API view that retrieves a single Topic object by its ID and
# serializes it using the TopicSerializer.
class DetailAPIView(generics.RetrieveAPIView):
    queryset=Topic.objects.all()
    serializer_class= TopicSerializer
    lookup_field= 'id'
    
# This is a Django REST framework class-based view that lists all instances of the Topic model and
# uses the TopicSerializer to serialize the data.
class ListAPIView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class= TopicSerializer
    pagination_class= LimitOffsetPagination
    filter_backends=[SearchFilter]
    search_fields=['blog_title','blog_summary']

# This is a Django REST framework view that creates a new blog topic and associates it with the
# authenticated user.
class blogCreate(generics.CreateAPIView):
    serializer_class= TopicSerializer
    def perform_create(self, serializer):
        # authenitcate() verifies and decode the token
        # if token is invalid, it raises an exception and returns 401
        # print(token.payload)
        # user = User.objects.get(pk=token.payload['user_id'])
        serializer.save(user=self.request.user)
    def get_queryset(self):
        queryset= Topic.objects.all()
        return queryset

# This is a Django REST framework class for updating a blog topic with a specified ID using a
# serializer.
class blogUpdate(generics.UpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset=Topic.objects.all()
    serializer_class= TopicSerializer
    lookup_field= 'id'
    def perform_update(self,serializer):
        instance= serializer.save()
        
# This is a Django REST framework class for deleting a blog post by its ID.
class blogDelete(generics.DestroyAPIView):
    queryset=Topic.objects.all()
    serializer_class= TopicSerializer
    lookup_field= 'id'
    
    def perform_destroy(self,instance):
        super().perform_destroy(instance)
    
    
# class productMixinView(mixins.UpdateModelMixin,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset=Topic.objects.all()
#     serializer_class= TopicSerializer
#     lookup_field="id"
    
#     def get(self,*args, **kwargs):
#         return self.list(request,*args, **kwargs)
     
#     def post(self,request,*args, **kwargs):
#         return self.create(request,*args, **kwargs)