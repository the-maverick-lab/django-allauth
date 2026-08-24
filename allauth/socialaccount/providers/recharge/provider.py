from __future__ import annotations

from django.http import HttpRequest

from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.recharge.views import RechargeOAuth2Adapter


# The parameters carrying the store domain on the install URL, one per
# ecommerce platform Recharge integrates with.
STORE_DOMAIN_PARAMS = ("myshopify_domain", "mybigcommerce_domain", "shop_domain")


class RechargeAccount(ProviderAccount):
    def to_str(self):
        if name := self.account.extra_data.get("name"):
            return name
        return super().to_str()


class RechargeProvider(OAuth2Provider):
    id = "recharge"
    name = "Recharge"
    account_class = RechargeAccount
    oauth2_adapter_class = RechargeOAuth2Adapter

    def extract_uid(self, data: dict) -> str:
        return str(data["store"]["id"])

    def extract_common_fields(self, data: dict) -> dict:
        ret: dict = {}
        store = self.extract_extra_data(data)
        if email := store.get("email"):
            ret["email"] = email
        if name := store.get("name"):
            ret["name"] = name
        return ret

    def extract_extra_data(self, data: dict) -> dict:
        return data["store"]

    def get_auth_params_from_request(self, request: HttpRequest, action):
        ret = super().get_auth_params_from_request(request, action)
        for param in STORE_DOMAIN_PARAMS:
            value = request.GET.get(param)
            if value:
                ret[param] = value
        return ret


provider_classes = [RechargeProvider]
providers.registry.register(RechargeProvider)
