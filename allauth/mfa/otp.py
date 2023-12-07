from django.contrib import messages

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.models import EmailAddress
from allauth.core import context
from allauth.mfa.adapter import get_adapter


OTP_SESSION_KEY = "mfa.otp"


def send_otp_by_mail(user):
    otp = context.request.session.get(OTP_SESSION_KEY)
    # FIXME: Improve generating/storing the OTP.
    # - OTP needs to be cleared when pressing "Cancel".
    # - Should also timeout
    # - And be tied to the current login session.
    if True or not otp:
        otp = get_adapter().generate_otp()
        context.request.session[OTP_SESSION_KEY] = otp
        email = EmailAddress.objects.get_primary_email(user)
        account_adapter = get_account_adapter()
        account_adapter.send_mail("mfa/email/otp_login", email, {"otp": otp})
        account_adapter.add_message(
            context.request,
            messages.SUCCESS,
            "mfa/messages/otp_sent.txt",
            message_context={"email": email},
        )


def validate_code(code):
    otp = context.request.session.get(OTP_SESSION_KEY)
    return code == otp
