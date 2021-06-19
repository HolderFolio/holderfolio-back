from django.urls import path, include

from dj_rest_auth.views  import PasswordResetConfirmView

from .api import (
    UserCreateView, GetAuthTokenAndData, GoogleLoginView, ManageUserView
)

app_name = 'user'

urlpatterns = [
    path('google-login/', GoogleLoginView.as_view(), name='user-login_google'),
    path('signup/', UserCreateView.as_view(), name='signup_user'),
    path('signin/', GetAuthTokenAndData.as_view(), name='signin_user'),
    path('me/', ManageUserView.as_view(), name='me_user'),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/password/reset/', PasswordResetConfirmView.as_view(), name='rest_password_reset'),
    path('dj-rest-auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  
]

