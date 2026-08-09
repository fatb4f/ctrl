from __future__ import annotations

from importlib.resources import files
from typing import Any

from handoff import handoff_schema
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError
from jsonschema.protocols import Validator
from pydantic import ValidationError as PydanticValidationError
from referencing import Registry, Resource

from .generated import SliceManifestProjection
from .jsonio import decode_object


class ContractDriftError(RuntimeError):
    pass


def _schema(name: str) -> dict[str, Any]:
    resource = files("runtime_promptgen.schemas").joinpath(name)
    return decode_object(resource.read_bytes(), label=f"packaged schema {name}")


SLICE_SCHEMA = _schema("slice-manifest.schema.json")
PROMPT_SCHEMA = _schema("prompt.schema.json")
HANDOFF_SCHEMA = handoff_schema()

Draft202012Validator.check_schema(SLICE_SCHEMA)
Draft202012Validator.check_schema(PROMPT_SCHEMA)
Draft202012Validator.check_schema(HANDOFF_SCHEMA)

_registry = Registry()
for schema in (SLICE_SCHEMA, HANDOFF_SCHEMA):
    _registry = _registry.with_resource(
        schema["$id"],
        Resource.from_contents(schema),
    )

_slice_validator = Draft202012Validator(SLICE_SCHEMA, format_checker=FormatChecker())
_prompt_validator = Draft202012Validator(
    PROMPT_SCHEMA,
    registry=_registry,
    format_checker=FormatChecker(),
)


def _validate(
    validator: Validator,
    document: dict[str, Any],
    *,
    label: str,
) -> None:
    errors = sorted(validator.iter_errors(document), key=lambda item: list(item.path))
    if not errors:
        return
    error: JSONSchemaValidationError = errors[0]
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    raise ValueError(f"{label} violates its schema at {location}: {error.message}")


def validate_slice(document: dict[str, Any]) -> SliceManifestProjection:
    _validate(_slice_validator, document, label="slice manifest")
    try:
        return SliceManifestProjection.model_validate(document)
    except PydanticValidationError as error:
        raise ContractDriftError(
            f"generated slice projection rejected a schema-valid document: {error}"
        ) from error


def validate_prompt(document: dict[str, Any]) -> None:
    _validate(_prompt_validator, document, label="runtime prompt")
