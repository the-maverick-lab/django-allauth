from django.http import HttpResponseRedirect
from django.urls import reverse

from allauth.account.stages import LoginStage
from allauth.mfa import app_settings, otp
from allauth.mfa.utils import is_mfa_enabled


class AuthenticateStage(LoginStage):
    key = "mfa_authenticate"

    def handle(self):
        response, cont = None, True
        if is_mfa_enabled(self.login.user):
            response = HttpResponseRedirect(reverse("mfa_authenticate"))
        elif app_settings.EMAIL_OTP:
            otp.send_otp_by_mail(self.login.user)
            response = HttpResponseRedirect(reverse("mfa_authenticate"))
        return response, cont
