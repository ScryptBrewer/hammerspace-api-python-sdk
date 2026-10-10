"""Base model shared by hand-written Hammerspace API payload models."""
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class HammerspaceBaseModel(BaseModel):
    """Base for Hammerspace API models.

    snake_case attributes map to camelCase wire keys via aliases
    (``site_uuid`` <-> ``siteUuid``); ``populate_by_name`` accepts either form on
    input; ``extra="allow"`` keeps parsing tolerant of fields added by newer
    appliance versions.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
        alias_generator=to_camel,
    )

    def to_api(self, **dump_kwargs: Any) -> Dict[str, Any]:
        """Serialize to the wire format: camelCase keys, only set fields, no Nones.

        ``mode="json"`` converts enums, datetimes and similar types to their
        JSON-safe representations so the payload can be sent as-is.
        """
        return self.model_dump(
            mode="json",
            by_alias=True,
            exclude_unset=True,
            exclude_none=True,
            **dump_kwargs,
        )
