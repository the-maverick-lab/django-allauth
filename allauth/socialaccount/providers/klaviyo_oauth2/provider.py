from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.klaviyo_oauth2.views import KlaviyoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class KlaviyoAccount(ProviderAccount):
    pass


class KlaviyoProvider(OAuth2Provider):
    id = "klaviyo_oauth2"
    name = "Klaviyo"
    account_class = KlaviyoAccount
    oauth2_adapter_class = KlaviyoOAuth2Adapter

    def extract_uid(self, data):
        return data.get("data", {})[0].get("id")

    def get_default_scope(self):
        return ["accounts:read"]


provider_classes = [KlaviyoProvider]
providers.registry.register(KlaviyoProvider)
