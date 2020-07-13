from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import register_view, user_activate, UserDetailView, \
    UserInfoChangeView, CompanyInfoChangeView, UserPasswordChangeView, UserListView, register_staff_view, \
    password_reset_email_view, PasswordResetFormView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('register_staff/', register_staff_view, name='register_staff'),
    path('register/activate/', user_activate, name='user_activate'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/list/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/update/', UserInfoChangeView.as_view(), name='user_update'),
    path('<int:pk>/company/', CompanyInfoChangeView.as_view(), name='company_update'),
    path('<int:pk>/password_change/', UserPasswordChangeView.as_view(), name='user_password_change'),
    path('reset-password/', password_reset_email_view, name='password_reset_email'),
    path('reset-password/<token>/', PasswordResetFormView.as_view(), name='password_reset_form')
]