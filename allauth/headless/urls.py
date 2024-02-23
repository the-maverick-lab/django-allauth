from django.urls import include, path, re_path

from allauth import app_settings as allauth_settings


_patterns = [
    path("", include("allauth.headless.base.urls")),
    path("", include("allauth.headless.account.urls")),
]

if allauth_settings.SOCIALACCOUNT_ENABLED:
    _patterns.append(path("", include("allauth.headless.socialaccount.urls")))

if allauth_settings.MFA_ENABLED:
    _patterns.append(path("", include("allauth.headless.mfa.urls")))

urlpatterns = [
    re_path(
        r"(?P<client>browser|device)/",
        include(_patterns),
    )
]
