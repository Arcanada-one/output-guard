"""Error hierarchy. Mirror of packages/ts/src/errors.ts."""

from __future__ import annotations


class ParseError(Exception):
    def __init__(self, message: str, cause: BaseException | None = None) -> None:
        super().__init__(message)
        self.__cause__ = cause


class SchemaValidationError(Exception):
    def __init__(self, message: str, issues: list[str] | None = None) -> None:
        super().__init__(message)
        self.issues: list[str] = list(issues or [])


class RepairError(Exception):
    def __init__(self, message: str, strategies_applied: list[str] | None = None) -> None:
        super().__init__(message)
        self.strategies_applied: list[str] = list(strategies_applied or [])


class GuardedGenerationError(Exception):
    def __init__(
        self,
        message: str,
        retries: int,
        last_error: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.retries: int = retries
        self.last_error: BaseException | None = last_error
