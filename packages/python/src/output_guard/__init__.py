"""arcanada-output-guard — LLM structured-output repair pipeline (Python).

Mirror surface of `@arcanada/output-guard` (TypeScript).
"""

from .adapters import SchemaAdapter, jsonschema_adapter, pydantic_adapter
from .batch import repair_batch, validate_batch
from .class_api import OutputGuard
from .constants import DEFAULT_TIMEOUT_MS, FORMAT_DEFAULT, MAX_RETRIES, RETRY_BACKOFF_MS
from .errors import (
    GuardedGenerationError,
    ParseError,
    RepairError,
    SchemaValidationError,
)
from .guarded_generate import GuardedGenerateOptions, guarded_generate
from .orchestrator import parse, repair, validate, validate_and_repair
from .results import (
    Format,
    GuardedGenerateResult,
    OrchestratorPass,
    RepairPass,
    RepairReport,
    RepairResult,
    ValidationResult,
)
from .retry_prompt import Message, RetryPromptOptions, RetryPromptResult, retry_prompt
from .strategies import CANONICAL_ORDER, STRATEGY_NAMES

__version__ = "0.1.0"

__all__ = [
    "CANONICAL_ORDER",
    "DEFAULT_TIMEOUT_MS",
    "FORMAT_DEFAULT",
    "MAX_RETRIES",
    "RETRY_BACKOFF_MS",
    "STRATEGY_NAMES",
    "Format",
    "GuardedGenerateOptions",
    "GuardedGenerateResult",
    "GuardedGenerationError",
    "Message",
    "OrchestratorPass",
    "OutputGuard",
    "ParseError",
    "RepairError",
    "RepairPass",
    "RepairReport",
    "RepairResult",
    "RetryPromptOptions",
    "RetryPromptResult",
    "SchemaAdapter",
    "SchemaValidationError",
    "ValidationResult",
    "__version__",
    "guarded_generate",
    "jsonschema_adapter",
    "parse",
    "pydantic_adapter",
    "repair",
    "repair_batch",
    "retry_prompt",
    "validate",
    "validate_and_repair",
    "validate_batch",
]
