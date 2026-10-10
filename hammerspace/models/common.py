"""Models shared across Hammerspace API resources."""
from typing import Any, Dict, List, Optional, Union

from .base import HammerspaceBaseModel


def extract_entity_uuid(ctx_map: Optional[Dict[str, Any]]) -> Optional[str]:
    """Extract the affected entity UUID from a task ``ctxMap``.

    Mirrors the appliance conventions previously hand-rolled in ``client.py``:
    the ``entity-uoid`` entry is either a dict carrying a ``uuid`` key or a flat
    string in which ``uuid=<value>`` appears among comma/bracket-joined fields.
    """
    if not ctx_map:
        return None
    entity_uoid = ctx_map.get("entity-uoid")
    if isinstance(entity_uoid, dict):
        uuid_value = entity_uoid.get("uuid")
        return str(uuid_value) if uuid_value else None
    if isinstance(entity_uoid, str) and "uuid=" in entity_uoid:
        try:
            parsed = entity_uoid.split("uuid=")[1].split(",")[0].split("]")[0].strip()
        except IndexError:
            return None
        return parsed or None
    return None


class TaskStatus(HammerspaceBaseModel):
    """Status payload polled from an async task's ``Location`` URL.

    The appliance fills any of ``state``/``status``/``statusMessage`` depending
    on the operation; ``effective_state`` normalizes them the same way the
    client's task monitor does.
    """

    uuid: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    status_message: Optional[str] = None
    progress_percent: Optional[Union[int, float, str]] = None
    error_message: Optional[str] = None
    ctx_map: Optional[Dict[str, Any]] = None

    @property
    def effective_state(self) -> str:
        value = self.state or self.status or self.status_message or ""
        return value.upper()

    @property
    def entity_uuid(self) -> Optional[str]:
        return self.uuid or extract_entity_uuid(self.ctx_map)


class TaskResult(HammerspaceBaseModel):
    """Result payload of a COMPLETED task (its ``result`` key or the task body)."""

    uuid: Optional[str] = None
    state: Optional[str] = None
    ctx_map: Optional[Dict[str, Any]] = None

    @property
    def entity_uuid(self) -> Optional[str]:
        return self.uuid or extract_entity_uuid(self.ctx_map)


class ApiErrorDetail(HammerspaceBaseModel):
    """One entry of the appliance's structured error response list."""

    error_code: Optional[str] = None
    message: Optional[str] = None
    args: Optional[List[Any]] = None
