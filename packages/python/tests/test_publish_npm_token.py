"""Require self-hosted npm publish via NPM_TOKEN (no GitHub-hosted OIDC).

Operator decision 2026-11-18: npm packages publish from our self-hosted runners
with an automation token held as secrets.NPM_TOKEN. Trusted Publishing / OIDC
is GitHub-hosted-only, so publish-npm.yml must not use ubuntu-*/macos-*/windows-*,
must drop id-token: write, must not pass --provenance, and must keep a dry-run
path that needs no secret.
"""

from __future__ import annotations

from pathlib import Path

import yaml

WORKFLOW = (
    Path(__file__).resolve().parents[3] / ".github" / "workflows" / "publish-npm.yml"
)
HOSTED_PREFIXES = ("ubuntu-", "macos-", "windows-")
REQUIRED_LABELS = {"self-hosted", "Linux", "X64", "ci-general"}


def _runs_on_values(raw: object) -> list[str]:
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, list):
        return [str(item) for item in raw]
    raise AssertionError(f"unexpected runs-on shape: {raw!r}")


def _job_scripts(job: dict) -> str:
    parts: list[str] = []
    for step in job.get("steps") or []:
        run = step.get("run")
        if isinstance(run, str):
            parts.append(run)
    return "\n".join(parts)


def test_publish_npm_refuses_github_hosted_runners() -> None:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    for job_name, job in doc["jobs"].items():
        labels = _runs_on_values(job["runs-on"])
        for label in labels:
            assert not label.startswith(HOSTED_PREFIXES), (
                f"publish-npm.yml job {job_name!r} runs-on includes GitHub-hosted "
                f"label {label!r}; use self-hosted labels {sorted(REQUIRED_LABELS)}"
            )
        assert set(labels) == REQUIRED_LABELS, (
            f"publish-npm.yml job {job_name!r} runs-on={labels!r}; "
            f"expected exactly {sorted(REQUIRED_LABELS)}"
        )


def test_publish_npm_uses_token_not_oidc() -> None:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    publish = doc["jobs"]["publish"]
    assert publish.get("environment") == "npm", (
        "NPM_TOKEN must be an environment secret from the npm environment"
    )
    perms = publish.get("permissions") or {}
    assert "id-token" not in perms, "publish must not request id-token: write"
    scripts = _job_scripts(publish)
    assert "--provenance" not in scripts, "provenance is unsupported off GitHub-hosted"
    assert "NODE_AUTH_TOKEN" in yaml.dump(publish), (
        "publish must bind NODE_AUTH_TOKEN from secrets.NPM_TOKEN"
    )
    assert "secrets.NPM_TOKEN" in yaml.dump(publish)


def test_npm_token_reference_is_limited_to_npm_environment_job() -> None:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    jobs_with_npm_secret = [
        name
        for name, job in doc["jobs"].items()
        if "secrets.NPM_TOKEN" in yaml.dump(job)
        or "NODE_AUTH_TOKEN" in yaml.dump(job)
    ]
    assert jobs_with_npm_secret == ["publish"]
    assert doc["jobs"]["publish"].get("environment") == "npm"


def test_publish_npm_never_publishes_on_pull_request() -> None:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    publish_if = str(doc["jobs"]["publish"].get("if") or "")
    assert "pull_request" not in publish_if
    assert "startsWith(github.ref, 'refs/tags/ts-v')" in publish_if
    assert "workflow_dispatch" not in publish_if
    assert "github.event_name == 'push'" in publish_if
    # PyYAML 1.1 coerces the workflow key `on` to boolean True.
    on = doc.get("on") or doc.get(True) or {}
    assert "pull_request" in on, "PR trigger required so dry-run runs in PR CI"


def test_publish_npm_refuses_manual_dispatch_and_checks_out_event_sha() -> None:
    """Manual refs cannot reach the token-bearing publish job."""
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    on = doc.get("on") or doc.get(True) or {}
    assert "workflow_dispatch" not in on, "manual ref publishing must be disabled"
    for job in doc["jobs"].values():
        checkouts = [
            step for step in job.get("steps", [])
            if step.get("uses", "").startswith("actions/checkout@")
        ]
        assert checkouts
        for checkout in checkouts:
            assert checkout.get("with", {}).get("ref") == "${{ github.sha }}"
            assert "inputs.ref" not in yaml.dump(checkout)


def test_publish_npm_requires_tokenless_tag_ancestor_gate() -> None:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    jobs = doc["jobs"]
    gate = jobs["tag-ancestor-gate"]
    gate_if = str(gate.get("if") or "")
    assert "github.event_name == 'push'" in gate_if
    assert "startsWith(github.ref, 'refs/tags/ts-v')" in gate_if

    checkout = next(
        step for step in gate["steps"]
        if step.get("uses", "").startswith("actions/checkout@")
    )
    assert checkout.get("with", {}).get("fetch-depth") == 0
    assert checkout.get("with", {}).get("ref") == "${{ github.sha }}"

    gate_script = _job_scripts(gate)
    assert "git fetch --no-tags origin +refs/heads/main:refs/remotes/origin/main" in gate_script
    assert 'git merge-base --is-ancestor "$GH_SHA" refs/remotes/origin/main' in gate_script
    assert "exit 1" in gate_script
    assert "NODE_AUTH_TOKEN" not in yaml.dump(gate)
    assert "secrets.NPM_TOKEN" not in yaml.dump(gate)

    publish = jobs["publish"]
    needs = publish.get("needs") or []
    assert "tag-ancestor-gate" in needs, "token-bearing publish must depend on ancestor gate"


def test_publish_npm_dry_run_job_needs_no_secret() -> None:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert "build" in doc["jobs"], "expected a build/dry-run job for PR CI"
    build = doc["jobs"]["build"]
    scripts = _job_scripts(build)
    assert "--dry-run" in scripts, "PR-safe path must run npm/pnpm publish --dry-run"
    assert "secrets.NPM_TOKEN" not in yaml.dump(build)
    assert "NODE_AUTH_TOKEN" not in yaml.dump(build)


def test_publish_npm_red_control_detects_ubuntu_latest() -> None:
    """Mutation stand: the assertion above must fail if ubuntu-latest returns."""
    fake = {"jobs": {"publish": {"runs-on": "ubuntu-latest"}}}
    labels = _runs_on_values(fake["jobs"]["publish"]["runs-on"])
    hosted = [label for label in labels if label.startswith(HOSTED_PREFIXES)]
    assert hosted == ["ubuntu-latest"]
