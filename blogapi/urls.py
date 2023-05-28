
from django.urls import path
from .views import api_home,blogCreate,blogUpdate,blogDelete,ListAPIView,DetailAPIView,MyObtainTokenPairView,RegisterView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("",api_home,name="api-home"),
    path("list/",ListAPIView.as_view(),name="blog-list"),
    path("detail/<int:id>", DetailAPIView.as_view(), name="blog-detail"),
    path("create", blogCreate.as_view(), name="blog-create"),
    path("update/<int:id>", blogUpdate.as_view(), name="blog-update"),
    path("delete/<int:id>", blogDelete.as_view(), name="blog-delete"),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',RegisterView.as_view(),name='auth_register')

] 