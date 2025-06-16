# hammerspace/i18n.py
import logging
from typing import Optional, Dict, Any
logger = logging.getLogger(__name__)

class I18nClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list_i18n_messages(self) -> Optional[Dict[str, Any]]: # Returns object with additionalProperties
        # GET /i18n
        path = "/i18n"
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)

    def get_i18n_messages_by_locale_name(self, locale_name: str) -> Optional[Dict[str, Any]]:
        # GET /i18n/{localeName}
        path = f"/i18n/{locale_name}"
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)