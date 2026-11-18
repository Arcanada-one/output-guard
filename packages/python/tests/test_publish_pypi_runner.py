"""Refuse GitHub-hosted runners on the PyPI publish workflow.

Operator order 2026-11-18: no GitHub-hosted runners anywhere. PyPI Trusted
Publishing is expected to work on self-hosted runners (OIDC), so
publish-pypi.yml must use the org self-hosted label set — not ubuntu-*/macos-*/
windows-*.
"""

from __future__ import annotations

from pathlib import Path

import yaml

WORKFLOW = (
    Path(__file__).resolve().parents[3] / ".github" / "workflows" / "publish-pypi.yml"
)
HOSTED_PREFIXES = ("ubuntu-", "macos-", "windows-")
REQUIRED_LABELS = {"self-hosted", "Linux", "X64", "ci-general"}


def _runs_on_values(raw: object) -> list[str]:
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, list):
        return [str(item) for item in raw]
    raise AssertionError(f"unexpected runs-on shape: {raw!r}")


def test_publish_pypi_refuses_github_hosted_runners() -> None:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    publish = doc["jobs"]["publish"]
    labels = _runs_on_values(publish["runs-on"])

    for label in labels:
        assert not label.startswith(HOSTED_PREFIXES), (
            f"publish-pypi.yml runs-on includes GitHub-hosted label {label!r}; "
            f"use self-hosted labels {sorted(REQUIRED_LABELS)}"
        )

    assert set(labels) == REQUIRED_LABELS, (
        f"publish-pypi.yml runs-on={labels!r}; expected exactly {sorted(REQUIRED_LABELS)}"
    )


def test_publish_pypi_red_control_detects_ubuntu_latest() -> None:
    """Mutation stand: the assertion above must fail if ubuntu-latest returns."""
    fake = {"jobs": {"publish": {"runs-on": "ubuntu-latest"}}}
    labels = _runs_on_values(fake["jobs"]["publish"]["runs-on"])
    hosted = [label for label in labels if label.startswith(HOSTED_PREFIXES)]
    assert hosted == ["ubuntu-latest"]
