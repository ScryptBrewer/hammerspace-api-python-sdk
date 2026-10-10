"""CrewAI tools for full Hammerspace cluster management.

Covers create/update/delete/manage across the main resources: shares,
objectives (SLAs), storage volumes, volume groups, users, sites, snapshots,
nodes, tasks — plus a generic ``api_call`` escape hatch to all 373 generated
SDK operations.

Guardrail: every destructive tool (delete/restore/move) requires an explicit
``confirm=True`` argument. Without it the tool refuses and the assistant must
ask the user first. ``build_tools(read_only=True)`` strips everything except
reads.
"""
import inspect
import json
import os
from typing import Any, List, Optional, Type

from pydantic import BaseModel, Field

try:
    from crewai.tools import BaseTool
except ImportError:  # older crewai
    from crewai_tools import BaseTool  # type: ignore

from hammerspace import HammerspaceApiClient

_client: Optional[HammerspaceApiClient] = None


def _get_client():
    global _client
    if _client is None:
        _client = HammerspaceApiClient(
            verify_ssl=os.getenv("VERIFY_SSL", "True").lower() in ("true", "1", "t"),
        )
    return _client


REFUSAL = (
    "REFUSED: this operation changes the cluster. Confirm with the user, then "
    "re-call this tool with confirm=true."
)


def _ok(result: Any, limit: int = 6000) -> str:
    text = json.dumps(result, indent=2, default=str)
    if len(text) > limit:
        text = text[:limit] + f"\n... (truncated, {len(text)} chars total)"
    return text


def _fail(exc: Exception) -> str:
    return f"[error] {type(exc).__name__}: {exc}"


class _NoInput(BaseModel):
    pass


class _IdentifierInput(BaseModel):
    identifier: str = Field(description="UUID or name of the object")


def _tool(name: str, description: str, args_model: Type[BaseModel], fn):
    """Build a BaseTool subclass wrapping fn (annotations required by pydantic)."""

    def _run(self, **kwargs):
        return _guarded(fn, kwargs)

    cls = type(
        f"_Tool_{name}",
        (BaseTool,),
        {
            "__module__": __name__,
            "__annotations__": {
                "name": str,
                "description": str,
                "args_schema": Type[BaseModel],
            },
            "name": name,
            "description": description,
            "args_schema": args_model,
            "_run": _run,
        },
    )
    return cls()


def _guarded(fn, kwargs):
    try:
        return fn(**kwargs)
    except Exception as exc:  # surface API errors to the LLM, never crash the loop
        return _fail(exc)


def _confirm_guard(kwargs) -> Optional[str]:
    if not kwargs.get("confirm"):
        return REFUSAL
    kwargs.pop("confirm", None)
    return None


class _ShareCreateInput(BaseModel):
    name: str = Field(description="Share name")
    path: str = Field(description="Export path of the share, e.g. /exports/docs")
    comment: Optional[str] = None
    share_size_limit: Optional[int] = Field(
        default=None, description="Max share size in bytes"
    )
    export_options: Optional[List[dict]] = Field(
        default=None,
        description='NFS export rules, e.g. [{"subnet": "*", "accessPermissions": "RW"}]',
    )
    share_objectives: Optional[List[dict]] = Field(
        default=None,
        description='SLA objectives to apply, e.g. [{"objective": {"name": "LAN"}}]',
    )


class _ShareUpdateInput(BaseModel):
    identifier: str = Field(description="Share UUID or name")
    fields: dict = Field(
        description="Partial share spec to apply (camelCase API fields), "
        'e.g. {"comment": "new", "shareSizeLimit": 1000000}'
    )


class _MoveShareInput(BaseModel):
    identifier: str = Field(description="Share UUID or name")
    destination: str = Field(description="Destination path for the share data")
    confirm: bool = Field(default=False, description="Must be true after user confirms")


class _DeleteInput(BaseModel):
    identifier: str = Field(description="UUID or name of the object to delete")
    confirm: bool = Field(default=False, description="Must be true after user confirms")


class _BodyInput(BaseModel):
    body: dict = Field(description="Request body using the API's camelCase spec fields")


class _BodyWithIdentifierInput(BaseModel):
    identifier: str = Field(description="UUID or name of the object")
    body: dict = Field(description="Request body using the API's camelCase spec fields")


class _SnapshotCreateInput(BaseModel):
    share_identifier: str = Field(description="Share UUID or name")
    snapshot_name: str = Field(description="Name for the new snapshot")


class _SnapshotInput(BaseModel):
    share_identifier: str = Field(description="Share UUID or name")
    snapshot_name: str = Field(description="Name of the snapshot")
    confirm: bool = Field(default=False, description="Must be true after user confirms")


class _RestoreInput(BaseModel):
    share_identifier: str = Field(description="Share UUID or name")
    snapshot_name: str = Field(description="Name of the snapshot to restore from")
    filename: Optional[str] = Field(
        default=None,
        description="Restore a single file instead of the whole share",
    )
    confirm: bool = Field(default=False, description="Must be true after user confirms")


class _UserCreateInput(BaseModel):
    username: str = Field(description="Login name of the new user")
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = Field(
        default=None, description='e.g. "ADMINISTRATOR", "MONITOR"'
    )


class _PasswordInput(BaseModel):
    identifier: str = Field(description="User UUID or name")
    password: str = Field(description="New password")


class _RemoteSiteInput(BaseModel):
    name: str = Field(description="Name of the remote site")
    address: str = Field(description="Hostname or IP of the remote appliance")
    username: Optional[str] = None
    password: Optional[str] = None
    confirm: bool = Field(default=False, description="Must be true after user confirms")


class _ApiCallInput(BaseModel):
    tag: str = Field(
        description='Resource tag, e.g. "shares", "nodes", "objectives", "licenses"'
    )
    method: str = Field(
        description='Generated method name, e.g. "list", "get", "create", "update", "delete"'
    )
    args_json: str = Field(
        default="{}",
        description='Keyword arguments as JSON, e.g. {"identifier": "abc"}',
    )
    confirm: bool = Field(
        default=False,
        description="Must be true for any write operation after user confirms",
    )


def _gen(tag: str):
    return getattr(_get_client().generated, tag)


# --------------------------------------------------------------- read tools


def _cluster_info() -> str:
    client = _get_client()
    info = {"system": client.system_info.get(raw=True)}
    try:
        info["local_site"] = client.generated.sites.get_local(raw=True)
    except Exception as exc:
        info["local_site"] = _fail(exc)
    return _ok(info)


def _list_nodes() -> str:
    return _ok(_gen("nodes").list(raw=True))


def _list_shares(identifier: Optional[str] = None) -> str:
    if identifier:
        return _ok(_gen("shares").get(identifier, raw=True))
    return _ok(_gen("shares").list(raw=True))


def _list_objectives() -> str:
    return _ok(_gen("objectives").list(raw=True))


def _list_storage_volumes() -> str:
    return _ok(_gen("storage-volumes").list(raw=True))


def _list_volume_groups() -> str:
    return _ok(_gen("volume-groups").list(raw=True))


def _list_users() -> str:
    return _ok(_gen("users").list(raw=True))


def _list_sites() -> str:
    return _ok(_gen("sites").list(raw=True))


def _get_tasks(identifier: Optional[str] = None) -> str:
    if identifier:
        return _ok(_gen("tasks").get(identifier, raw=True))
    return _ok(_gen("tasks").list(raw=True))


def _list_share_snapshots(share_identifier: str) -> str:
    return _ok(_gen("share-snapshots").snapshot_list(share_identifier, raw=True))


# ------------------------------------------------------------ write tools


def _create_share(
    name: str,
    path: str,
    comment: Optional[str] = None,
    share_size_limit: Optional[int] = None,
    export_options: Optional[List[dict]] = None,
    share_objectives: Optional[List[dict]] = None,
) -> str:
    from hammerspace.models.share import ShareCreate

    body = ShareCreate(
        name=name,
        path=path,
        comment=comment,
        share_size_limit=share_size_limit,
        export_options=export_options,
        share_objectives=share_objectives,
    )
    return _ok(_gen("shares").create(body=body.to_api(), raw=True))


def _update_share(identifier: str, fields: dict) -> str:
    return _ok(_gen("shares").update(identifier, body=fields, raw=True))


def _delete_share(identifier: str, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(_gen("shares").delete(identifier, raw=True))


def _move_share(identifier: str, destination: str, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(_gen("shares").move(identifier, destination, raw=True))


def _create_objective(body: dict) -> str:
    return _ok(_gen("objectives").create(body=body, raw=True))


def _delete_objective(identifier: str, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(_gen("objectives").delete(identifier, raw=True))


def _create_storage_volume(body: dict) -> str:
    return _ok(_gen("storage-volumes").create(body=body, raw=True))


def _delete_storage_volume(identifier: str, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(_gen("storage-volumes").delete(identifier, raw=True))


def _create_volume_group(body: dict) -> str:
    return _ok(_gen("volume-groups").create(body=body, raw=True))


def _delete_volume_group(identifier: str, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(_gen("volume-groups").delete(identifier, raw=True))


def _create_user(username: str, full_name: Optional[str] = None,
                 email: Optional[str] = None, role: Optional[str] = None) -> str:
    body = {"username": username, "fullName": full_name or username, "type": role}
    return _ok(_gen("users").create(body={k: v for k, v in body.items() if v}, raw=True))


def _set_user_password(identifier: str, password: str) -> str:
    return _ok(_gen("users").update_password(identifier, body={"password": password}, raw=True))


def _delete_user(identifier: str, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(_gen("users").delete(identifier, raw=True))


def _add_remote_site(name: str, address: str, username: Optional[str] = None,
                     password: Optional[str] = None, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    body = {"name": name, "address": address}
    if username:
        body["username"] = username
    if password:
        body["password"] = password
    return _ok(_gen("sites").add_remote_site(body=body, raw=True))


def _delete_site(identifier: str, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(_gen("sites").delete(identifier, raw=True))


def _create_share_snapshot(share_identifier: str, snapshot_name: str) -> str:
    return _ok(
        _gen("share-snapshots").snapshot_create(share_identifier, snapshot_name, raw=True)
    )


def _restore_share_snapshot(share_identifier: str, snapshot_name: str,
                            filename: Optional[str] = None, confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(
        _gen("share-snapshots").snapshot_restore(
            share_identifier, snapshot_name, filename=filename, raw=True
        )
    )


def _delete_share_snapshot(share_identifier: str, snapshot_name: str,
                           confirm: bool = False) -> str:
    if not confirm:
        return REFUSAL
    return _ok(
        _gen("share-snapshots").snapshot_delete(share_identifier, snapshot_name, raw=True)
    )


def _api_call(tag: str, method: str, args_json: str = "{}", confirm: bool = False) -> str:
    try:
        kwargs = json.loads(args_json or "{}")
    except json.JSONDecodeError as exc:
        return f"[error] args_json is not valid JSON: {exc}"
    if tag not in _known_tags():
        return f"[error] unknown tag {tag!r}; known tags: {sorted(_known_tags())}"
    client_obj = _gen(tag)
    fn = getattr(client_obj, method, None)
    if fn is None or method.startswith("_"):
        methods = [
            n for n, m in inspect.getmembers(client_obj, inspect.ismethod)
            if not n.startswith("_")
        ]
        return f"[error] unknown method {method!r} on {tag!r}; known: {methods}"
    mutating = "monitor_task" in inspect.signature(fn).parameters
    if mutating and not confirm:
        return REFUSAL
    try:
        return _ok(fn(**kwargs, raw=True))
    except Exception as exc:
        return _fail(exc)


def _known_tags():
    from hammerspace.generated import TAG_MODULES

    return TAG_MODULES


# ---------------------------------------------------------------- assembly


def _make_lookup_input():
    class _LookupInput(BaseModel):
        identifier: Optional[str] = Field(
            default=None, description="Optional UUID or name to fetch a single share"
        )
    return _LookupInput


def build_tools(read_only: bool = False) -> list:
    """Assemble the cluster-management toolset.

    read_only=True keeps only the inspection tools; otherwise the full
    create/update/delete/manage toolset is returned (destructive ops still
    require confirm=true at call time).
    """
    if not os.getenv("HS_BASE_URL"):
        raise SystemExit(
            "Hammerspace tools require HS_BASE_URL (and HS_USERNAME/HS_PASSWORD) "
            "in the environment or .env file."
        )
    specs = [
        # name, description, args model, fn
        ("cluster_info", "Get Hammerspace cluster overview: software version, local "
         "site and general system info.", _NoInput, _cluster_info),
        ("list_nodes", "List storage nodes with state and hardware details.",
         _NoInput, _list_nodes),
        ("list_shares", "List all file shares, or fetch one share by UUID/name.",
         _make_lookup_input(), _list_shares),
        ("list_objectives", "List data policy objectives (SLAs) such as LAN, WAN, "
         "performance tiers.", _NoInput, _list_objectives),
        ("list_storage_volumes", "List backend storage volumes.",
         _NoInput, _list_storage_volumes),
        ("list_volume_groups", "List volume groups.", _NoInput, _list_volume_groups),
        ("list_users", "List appliance users.", _NoInput, _list_users),
        ("list_sites", "List local and remote sites in the global namespace.",
         _NoInput, _list_sites),
        ("get_tasks", "List recent cluster tasks, or fetch one task by UUID "
         "(use after any create/update/delete to check completion).",
         _make_lookup_input(), _get_tasks),
        ("list_share_snapshots", "List snapshots of a share.",
         _make_snapshot_list_input(), _list_share_snapshots),
    ]
    if not read_only:
        specs += [
            ("create_share", "Create a new file share with optional export rules "
             "and SLA objectives.", _ShareCreateInput, _create_share),
            ("update_share", "Update an existing share with a partial spec.",
             _ShareUpdateInput, _update_share),
            ("delete_share", "Delete a share. DESTRUCTIVE - requires confirm=true.",
             _DeleteInput, _delete_share),
            ("move_share", "Move share data to a new destination path. "
             "DESTRUCTIVE - requires confirm=true.", _MoveShareInput, _move_share),
            ("create_objective", "Create a data policy objective (SLA) from a "
             "spec body.", _BodyInput, _create_objective),
            ("delete_objective", "Delete an objective (SLA). DESTRUCTIVE - "
             "requires confirm=true.", _DeleteInput, _delete_objective),
            ("create_storage_volume", "Add a backend storage volume to the "
             "cluster from a spec body.", _BodyInput, _create_storage_volume),
            ("delete_storage_volume", "Remove a backend storage volume. "
             "DESTRUCTIVE - requires confirm=true.", _DeleteInput,
             _delete_storage_volume),
            ("create_volume_group", "Create a volume group from a spec body.",
             _BodyInput, _create_volume_group),
            ("delete_volume_group", "Delete a volume group. DESTRUCTIVE - "
             "requires confirm=true.", _DeleteInput, _delete_volume_group),
            ("create_user", "Create an appliance user.", _UserCreateInput,
             _create_user),
            ("set_user_password", "Set or reset a user's password.",
             _PasswordInput, _set_user_password),
            ("delete_user", "Delete a user. DESTRUCTIVE - requires confirm=true.",
             _DeleteInput, _delete_user),
            ("add_remote_site", "Pair a remote Hammerspace appliance into the "
             "global namespace. Changes topology - requires confirm=true.",
             _RemoteSiteInput, _add_remote_site),
            ("delete_site", "Remove a site from the global namespace. "
             "DESTRUCTIVE - requires confirm=true.", _DeleteInput, _delete_site),
            ("create_share_snapshot", "Create a snapshot of a share.",
             _SnapshotCreateInput, _create_share_snapshot),
            ("restore_share_snapshot", "Restore a share (or single file) from a "
             "snapshot, overwriting current data. DESTRUCTIVE - requires "
             "confirm=true.", _RestoreInput, _restore_share_snapshot),
            ("delete_share_snapshot", "Delete a share snapshot. DESTRUCTIVE - "
             "requires confirm=true.", _SnapshotInput, _delete_share_snapshot),
            ("api_call", "Call ANY generated SDK operation for full cluster "
             "coverage: tags like licenses, network_interfaces, kmses, ntps, "
             "dnss, idp, syslog, sw_update; methods like list/get/create/update/"
             "delete. Write operations require confirm=true. args_json holds "
             "keyword args.", _ApiCallInput, _api_call),
        ]
    return [_tool(name, desc, model, fn) for name, desc, model, fn in specs]


def _make_snapshot_list_input():
    class _SnapshotListInput(BaseModel):
        share_identifier: str = Field(description="Share UUID or name")
    return _SnapshotListInput
