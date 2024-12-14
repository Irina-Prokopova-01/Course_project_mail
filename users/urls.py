from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page
from users.apps import UsersConfig
from users.views import RegisterView, email_verification, UsersListView, UserPasswordResetConfirmView, BlockUserView, UnblockUserView, UserDetailView, UserUpdateView, UserForgotPasswordView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name="logout"),
    path('register/', RegisterView.as_view(template_name="users/register.html"), name='register'),
    path("password-reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path('email-confirm/<str:token>/', email_verification, name='email_verification'),
    path("set-new-password/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("users_list/", UsersListView.as_view(), name="users_list"),
    path("users/<int:pk>/block", BlockUserView.as_view(), name="users_block"),
    path("users/<int:pk>/unblock", UnblockUserView.as_view(), name="users_unblock"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="users_detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="users_update"),
]