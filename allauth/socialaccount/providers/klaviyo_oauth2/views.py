import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


KLAVIYO_API_VERSION = "2023-10-15"


class KlaviyoOAuth2Adapter(OAuth2Adapter):
    provider_id = "klaviyo_oauth2"
    basic_auth = True

    @property
    def access_token_url(self):
        return "https://a.klaviyo.com/oauth/token"

    @property
    def authorize_url(self):
        return "https://www.klaviyo.com/oauth/authorize"

    def complete_login(self, request, app, access_token, **kwargs):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "revision": KLAVIYO_API_VERSION,
            "Authorization": f"Bearer {access_token.token}",
        }
        r = requests.get(
            "https://a.klaviyo.com/api/accounts/",
            headers=headers,
        )
        extra_data = r.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(KlaviyoOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(KlaviyoOAuth2Adapter)
