from django.urls import path, re_path

# from allauth.account.views import SignupView, LoginView, LogoutView

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, LogoutView
from allauth.account.views import confirm_email
from .views import AccountEmailVerificationSentView



urlpatterns = [

    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="login"),
    re_path(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$',
            confirm_email, name='account_confirm_email'),
    path('account-email-verification-sent/', AccountEmailVerificationSentView.as_view(),
         name='account_email_verification_sent'),

]