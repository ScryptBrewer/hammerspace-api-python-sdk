#!/usr/bin/env python3
"""Generate spec-coverage API clients from the vendored Hammerspace swagger.

Reads the Swagger 2.0 spec and emits one client module per tag under
``hammerspace/generated/`` plus a registry exposing ``GeneratedApiNamespace``.
Hand-written modules under ``hammerspace/`` remain the curated surface; the
generated package adds complete typed coverage of every tagged operation.

Method naming (see PYDANTIC_MIGRATION_PLAN.md, Phase 4b): operationIds are not
unique (133 unique across 373 operations; get x56, list x56, ...), so names are
derived from method + path, preferring a semantic operationId when it is not a
generic verb:

    GET  /x                     -> list
    GET  /x/{identifier}        -> get
    GET  /x/{identifier}/<tail> -> list_<tail>
    POST /x                     -> create
    POST /x/<action>            -> <action>          (e.g. flush_cache)
    POST /x/<tail>              -> create_<tail>
    PUT  /x/{identifier}        -> update
    DELETE /x/{identifier}      -> delete

Collisions inside a class are resolved by appending the distinguishing path
segment, then a numeric suffix.

Usage:
    python tools/generate_clients.py \
        --spec Hammerspace_5_3_swagger.json \
        --out-dir hammerspace/generated
"""
from __future__ import annotations

import argparse
import json
import keyword
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HTTP_METHODS = ("get", "post", "put", "delete", "patch")
GENERIC_OPERATION_IDS = {
    "get", "list", "put", "post", "delete", "create", "update",
    "add", "remove", "get_all", "list_all", "backup_restore",
}


def to_snake(name: str) -> str:
    """kebab-case / camelCase / dotted name -> python identifier."""
    name = name.replace("-", "_").replace(".", "_")
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    name = re.sub(r"_+", "_", name).strip("_").lower()
    if not name:
        name = "param"
    if name[0].isdigit():
        name = f"p_{name}"
    if keyword.iskeyword(name):
        name = f"{name}_"
    return name


def to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in to_snake(name).split("_"))


def ref_model_name(schema: Dict[str, Any]) -> Optional[str]:
    """Model class name referenced by a schema (or its array items)."""
    if not isinstance(schema, dict):
        return None
    ref = schema.get("$ref")
    if not ref and schema.get("type") == "array":
        ref = (schema.get("items") or {}).get("$ref")
    if not ref:
        return None
    return ref.rsplit("/", 1)[-1] if "/" in ref else None


class Generator:
    def __init__(self, spec: Dict[str, Any], valid_models: set):
        self.spec = spec
        self.valid_models = valid_models

    # ---------------------------------------------------------------- naming

    def method_name(self, http_method: str, path: str, op: Dict[str, Any],
                    taken: set) -> str:
        segments = [s for s in path.split("/") if s]
        tail = segments[-1]
        tail_is_param = tail.startswith("{")
        operation_id = to_snake(op.get("operationId") or "")

        base: Optional[str] = None
        if operation_id and operation_id not in GENERIC_OPERATION_IDS:
            base = operation_id
        if base is None:
            tail_literal = None if tail_is_param else to_snake(tail)
            if http_method == "get":
                base = "get" if tail_is_param else "list"
            elif http_method == "post":
                if tail_is_param:
                    base = "create"
                elif tail_literal and tail_literal != to_snake(segments[0]):
                    base = tail_literal
                else:
                    base = "create"
            elif http_method == "put":
                base = "update"
            elif http_method == "delete":
                base = "delete"
            else:
                base = http_method

        name = base
        if name in taken:
            # First collision: append the distinguishing path segment.
            distinguishing = None
            for segment in reversed(segments[:-1]):
                if not segment.startswith("{"):
                    candidate = to_snake(segment)
                    if candidate and candidate != base:
                        distinguishing = candidate
                        break
            if distinguishing:
                name = f"{base}_{distinguishing}"
        counter = 2
        while name in taken:
            name = f"{base}_{counter}"
            counter += 1
        taken.add(name)
        return name

    # --------------------------------------------------------------- params

    def op_params(
        self, op: Dict[str, Any]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Optional[Dict[str, Any]]]:
        path_params, query_params, body = [], [], None
        for param in op.get("parameters", []):
            location = param.get("in")
            if location == "path":
                path_params.append(param)
            elif location == "query":
                query_params.append(param)
            elif location == "body":
                body = param
        return path_params, query_params, body

    def arg_name(self, wire_name: str, used: set) -> Tuple[str, str]:
        """Return (python_arg, wire_name), deduping against used args."""
        arg = to_snake(wire_name)
        while arg in used or arg in ("self", "raw", "body", "monitor_task",
                                     "task_timeout_seconds", "path"):
            arg = f"{arg}_param"
        used.add(arg)
        return arg, wire_name

    # -------------------------------------------------------------- emission

    def emit_operation(self, http_method: str, path: str, op: Dict[str, Any],
                       taken: set) -> str:
        name = self.method_name(http_method, path, op, taken)
        path_params, query_params, body_param = self.op_params(op)
        body_model = ref_model_name((body_param or {}).get("schema") or {})
        body_model = body_model if body_model in self.valid_models else None
        resp_200 = (op.get("responses") or {}).get("200") or {}
        response_model = ref_model_name(resp_200.get("schema") or {})
        response_model = response_model if response_model in self.valid_models else None

        resolved: Dict[str, str] = {}
        used_args: set = set()
        args: List[str] = []
        for param in path_params + query_params:
            arg, _ = self.arg_name(param["name"], used_args)
            resolved[param["name"]] = arg
        for param in path_params:
            args.append(f"{resolved[param['name']]}: str")
        for param in query_params:
            args.append(f"{resolved[param['name']]}: Optional[Any] = None")
        if body_param is not None:
            if body_model:
                args.append(f"body: Optional[gen.{body_model}] = None")
            else:
                args.append("body: Optional[Any] = None")
        args.append("monitor_task: bool = True")
        args.append("task_timeout_seconds: int = 300")
        args.append("raw: bool = False")
        signature = ", ".join(["self"] + args)

        if response_model:
            returns = f"Union[List[gen.{response_model}], gen.{response_model}, Any]"
        else:
            returns = "Any"

        lines: List[str] = []
        summary = (op.get("summary") or op.get("description") or "").strip()
        lines.append(f"    def {name}({signature}) -> {returns}:")
        docline = summary.splitlines()[0] if summary else f"{http_method.upper()} {path}"
        lines.append(f"        {docline!r}")

        path_expr = repr(path)
        if path_params:
            py_path = path
            for param in path_params:
                py_path = py_path.replace(
                    "{" + param["name"] + "}",
                    "{_urlquote(" + resolved[param["name"]] + ", safe='')}",
                )
            path_expr = f'f"{py_path}"'

        lines.append("        query_params = {}")
        for param in query_params:
            arg = resolved[param["name"]]
            lines.append(f"        if {arg} is not None: query_params[{param['name']!r}] = {arg}")

        if http_method == "get":
            model_arg = f"model=gen.{response_model}, " if response_model else ""
            lines.append(
                f"        response = self.api_client.make_rest_call("
                f"path={path_expr}, method=\"GET\", query_params=query_params, "
                f"{model_arg}raw=raw)"
            )
            lines.append(
                f"        return self.api_client.read_and_parse_json_body("
                f"response, {model_arg}raw=raw)"
            )
        else:
            model_arg = f"gen.{response_model}" if response_model else "None"
            lines.append("        return self.api_client.execute_and_monitor_task(")
            lines.append(f"            path={path_expr},")
            lines.append(f'            method="{http_method.upper()}",')
            if body_param is not None:
                lines.append("            initial_json_data=body,")
            if query_params:
                lines.append("            initial_query_params=query_params,")
            lines.append("            monitor_task=monitor_task,")
            lines.append("            task_timeout_seconds=task_timeout_seconds,")
            lines.append(f"            result_model=None if raw else {model_arg},")
            lines.append("            raw=raw,")
            lines.append("        )")
        return "\n".join(lines)

    def emit_tag_module(self, tag: str, ops: List[Tuple[str, str, Dict[str, Any]]]) -> str:
        class_name = f"Generated{to_pascal(tag)}Client"
        taken: set = set()
        methods = [
            self.emit_operation(http_method, path, op, taken)
            for http_method, path, op in sorted(ops, key=lambda item: (item[1], item[0]))
        ]
        methods_text = "\n\n".join(methods)
        typing_names = [
            n for n in ("Dict", "List", "Optional", "Union") if f"{n}[" in methods_text
        ]
        header_lines = [
            f'"""Spec-generated client for the "{tag}" API tag. Do not edit.',
            "",
            "Regenerate with: python tools/generate_clients.py",
            '"""',
            "from typing import Any" + (", " + ", ".join(typing_names) if typing_names else ""),
        ]
        if any("{" in p for _, p, _ in ops):
            header_lines.append("from urllib.parse import quote as _urlquote")
        header_lines.extend(
            [
                "",
                "from hammerspace.models import generated as gen",
                "",
                "",
                f"class {class_name}:",
                f'    """Typed coverage for all {len(ops)} "{tag}" operations."""',
                "",
                "    def __init__(self, api_client: Any):",
                "        self.api_client = api_client",
            ]
        )
        return "\n".join(header_lines) + "\n\n" + methods_text + "\n"

    def run(self, out_dir: Path) -> Dict[str, int]:
        grouped: Dict[str, List[Tuple[str, str, Dict[str, Any]]]] = {}
        for path, path_ops in self.spec.get("paths", {}).items():
            for http_method, op in path_ops.items():
                if http_method not in HTTP_METHODS or not isinstance(op, dict):
                    continue
                tag = (op.get("tags") or [path.strip("/").split("/")[0]])[0]
                grouped.setdefault(tag, []).append((http_method, path, op))

        out_dir.mkdir(parents=True, exist_ok=True)
        registry_entries = []
        total_methods = 0
        for tag in sorted(grouped):
            module_name = to_snake(tag)
            class_name = f"Generated{to_pascal(tag)}Client"
            module_source = self.emit_tag_module(tag, grouped[tag])
            (out_dir / f"{module_name}.py").write_text(module_source)
            registry_entries.append((module_name, class_name, tag))
            total_methods += len(grouped[tag])

        registry_lines = [
            '"""Registry of spec-generated API clients. Do not edit.\n\n'
            "Regenerate with: python tools/generate_clients.py\n"
            '"""',
            "import importlib",
            "from typing import Any, Dict, List\n",
        ]
        registry_lines.append("TAG_MODULES: Dict[str, str] = {")
        for module_name, _, tag in registry_entries:
            registry_lines.append(f"    {tag!r}: {module_name!r},")
        registry_lines.append("}")
        registry_lines.append("")
        registry_lines.append("_CLASS_NAMES: Dict[str, str] = {")
        for _, class_name, tag in registry_entries:
            registry_lines.append(f"    {tag!r}: {class_name!r},")
        registry_lines.append("}")
        registry_lines.extend([
            "",
            "",
            "def get_client_class(tag: str) -> type:",
            '    """Import and return the generated client class for ``tag`` (lazily)."""',
            "    module_name = TAG_MODULES.get(tag)",
            "    if module_name is None:",
            "        raise KeyError(",
            "            f'No generated client for {tag!r}; known tags: {sorted(TAG_MODULES)}'",
            "        )",
            "    module = importlib.import_module('hammerspace.generated.' + module_name)",
            "    return getattr(module, _CLASS_NAMES[tag])",
            "",
            "",
            "class GeneratedApiNamespace:",
            '    """Lazy namespace: ``client.generated.<tag>`` -> typed client.',
            "",
            "    Each tag module is imported on first access, so touching one tag",
            "    does not pay the import cost of the other 68.",
            '    """',
            "",
            "    def __init__(self, api_client: Any):",
            "        self._api_client = api_client",
            "",
            "    def __getattr__(self, name: str) -> Any:",
            "        if name not in TAG_MODULES:",
            "            raise AttributeError(",
            "                f'No generated client for {name!r}; "
            "known tags: {sorted(TAG_MODULES)}'",
            "            ) from None",
            "        instance = get_client_class(name)(self._api_client)",
            "        setattr(self, name, instance)",
            "        return instance",
            "",
            "    def __dir__(self) -> List[str]:",
            "        return sorted(set(super().__dir__()) | set(TAG_MODULES))",
            "",
            "",
            "__all__ = [\"TAG_MODULES\", \"get_client_class\", \"GeneratedApiNamespace\"]",
            "",
        ])
        (out_dir / "__init__.py").write_text("\n".join(registry_lines))
        return {"tags": len(registry_entries), "operations": total_methods}


def main() -> None:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", default="Hammerspace_5_3_swagger.json")
    parser.add_argument("--out-dir", default="hammerspace/generated")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text())

    from hammerspace.models import generated as generated_models

    valid_models = {
        name for name in dir(generated_models)
        if isinstance(getattr(generated_models, name), type)
    }
    stats = Generator(spec, valid_models).run(Path(args.out_dir))
    print(
        f"generated {stats['tags']} client modules, "
        f"{stats['operations']} methods -> {args.out_dir}"
    )


if __name__ == "__main__":
    main()
