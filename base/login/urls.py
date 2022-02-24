from django.urls import path
from .views import home, LoginFormView, LogoutFormView, RegisterFormView, ListUserFormView, UserUpdateView, UserDeleteView


app_name = "session"

urlpatterns = [
	path('', LoginFormView.as_view(), name='login'),
	path('user/logout/', LogoutFormView.as_view(), name='logout'),
	path('user/list/', ListUserFormView.as_view(), name='list'),
	path('user/register/', RegisterFormView.as_view(), name='register'),
	path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
	path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
]
