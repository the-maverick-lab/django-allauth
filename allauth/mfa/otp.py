from django.contrib import messages

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.models import EmailAddress
from allauth.core import context
from allauth.mfa.adapter import get_adapter


def send_otp_by_mail(user, state):
    otp = state.get("otp")
    if not otp:
        otp = get_adapter().generate_otp()
        state["otp"] = otp
        email = EmailAddress.objects.get_primary_email(user)
        account_adapter = get_account_adapter()
        account_adapter.send_mail("mfa/email/otp_login", email, {"otp": otp})
        account_adapter.add_message(
            context.request,
            messages.SUCCESS,
            "mfa/messages/otp_sent.txt",
            message_context={"email": email},
        )


def validate_code(code, state):
    otp = state.get("otp")
    return otp and code == otp
