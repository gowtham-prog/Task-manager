from django.urls import path

from .views import UserCreateAPIView,UserUpdateAPIView,UserRetrieveAPIView, LogoutView
urlpatterns = [
    path("user/create", UserCreateAPIView.as_view(), name="user_create"),
    path("user/get", UserUpdateAPIView.as_view(), name="user_update"),
    path("user/update", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("logout/", LogoutView.as_view(), name="logout"),
]