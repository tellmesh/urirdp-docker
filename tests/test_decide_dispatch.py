"""Characterization tests for urillm.handlers.text_decide dispatch (no network)."""

from __future__ import annotations

import urillm.handlers as h


def _cfg(driver: str, **extra) -> dict:
    return {"config": {"llm": {"driver": driver, **extra}}}


def test_missing_question_errors():
    assert h.text_decide({}, {}) == {"ok": False, "error": "payload.question is required"}


def test_mock_retry_on_critical_pattern():
    out = h.text_decide({"question": "retry?", "context": {"log": "error 502"}}, _cfg("mock"))
    assert out["decision"] == "retry" and out["ok"] is True
    assert out["model"] == "mock-decide"


def test_mock_abort_on_clean_context():
    out = h.text_decide({"question": "retry?", "context": {"log": "all good"}}, _cfg("mock"))
    assert out["decision"] == "abort" and out["ok"] is False


def test_dry_run_forces_mock():
    ctx = {"dry_run": True, **_cfg("openai")}
    out = h.text_decide({"question": "q", "context": {"e": "502"}}, ctx)
    assert out["model"] == "mock-decide" and out["decision"] == "retry"


def test_real_driver_without_credentials_falls_back(monkeypatch):
    for key in ("OPENROUTER_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    ctx = {"allow_real": True, **_cfg("openai")}
    out = h.text_decide({"question": "q"}, ctx)
    assert out["model"] == "mock-decide"


def test_unknown_driver_falls_back_to_mock():
    ctx = {"allow_real": True, **_cfg("weird", model="m", api_key="k")}
    out = h.text_decide({"question": "q", "context": {"e": "error"}}, ctx)
    assert out["model"] == "mock-decide"
