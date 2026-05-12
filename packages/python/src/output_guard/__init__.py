"""arcanada-output-guard — LLM structured-output repair pipeline (Python).

M1 bootstrap: constants + result/error types only. Implementation lands in M3 (CONN-0087).
Mirror surface of `@arcanada/output-guard` (TypeScript).
"""

from .constants import DEFAULT_TIMEOUT_MS, FORMAT_DEFAULT, MAX_RETRIES, RETRY_BACKOFF_MS
from .errors import (
    GuardedGenerationError,
    ParseError,
    RepairError,
    SchemaValidationError,
)
from .results import (
    Format,
    GuardedGenerateResult,
    OrchestratorPass,
    RepairReport,
    RepairResult,
    ValidationResult,
)

__version__ = "0.0.1"

__all__ = [
    "DEFAULT_TIMEOUT_MS",
    "FORMAT_DEFAULT",
    "MAX_RETRIES",
    "RETRY_BACKOFF_MS",
    "Format",
    "GuardedGenerateResult",
    "GuardedGenerationError",
    "OrchestratorPass",
    "ParseError",
    "RepairError",
    "RepairReport",
    "RepairResult",
    "SchemaValidationError",
    "ValidationResult",
    "__version__",
]
