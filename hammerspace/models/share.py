"""Models for the Hammerspace shares API (ShareView family).

``ShareView`` extends the codegen ``models.generated.ShareView`` (single source
of truth for the field set) and layers on the curated conveniences: plain-string
``share_state`` and a ``uuid`` property that also surfaces task-result payloads
(``{"uuid": ...}``) which the wire nests nowhere else. Unknown fields are
tolerated (``extra="allow"``) so responses from newer appliance versions still
parse.
"""
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from .base import HammerspaceBaseModel
from .generated import ShareView as _GeneratedShareView


class ExportOption(HammerspaceBaseModel):
    """One NFS export rule of a share (``ExportOptionsView``)."""

    id: Optional[int] = None
    subnet: Optional[str] = None
    access_permissions: Optional[str] = Field(default=None, description="RO or RW")
    security_options: Optional[List[str]] = None
    root_squash: Optional[bool] = None
    insecure: Optional[bool] = None


class ShareObjective(HammerspaceBaseModel):
    """An objective applied to a share (``ShareObjectiveView``)."""

    objective: Optional[Dict[str, Any]] = None
    applicability: Optional[str] = None
    removable: Optional[bool] = None


class ShareView(_GeneratedShareView):
    """Read model for ``GET /shares`` responses (``ShareView``)."""

    share_state: Optional[str] = None

    @property
    def uuid(self) -> Optional[str]:
        """Entity UUID: nested in ``uoid``, or top-level in task results."""
        uoid = self.uoid
        if isinstance(uoid, dict):
            nested = uoid.get("uuid")
            if nested is not None:
                return nested
        elif uoid is not None:
            nested = getattr(uoid, "uuid", None)
            if nested is not None:
                return nested
        if self.model_extra:
            return self.model_extra.get("uuid")
        return None


class ShareUpdate(HammerspaceBaseModel):
    """Write model for ``PUT /shares/{identifier}``; all fields optional."""

    name: Optional[str] = None
    path: Optional[str] = None
    comment: Optional[str] = None
    export_options: Optional[List[Union[ExportOption, Dict[str, Any]]]] = None
    share_objectives: Optional[List[Union[ShareObjective, Dict[str, Any]]]] = None
    share_size_limit: Optional[int] = None
    warn_utilization_percent_threshold: Optional[int] = None
    smb_browsable: Optional[bool] = None


class ShareCreate(ShareUpdate):
    """Write model for ``POST /shares``; name and path are required."""

    name: str
    path: str
