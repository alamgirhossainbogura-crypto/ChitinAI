import pytest
from chitin.watcher import AgentWatcher
from chitin.memory.ccloud_cli import CockroachAutoHealer

def test_watcher_hallucination_detection():
    watcher = AgentWatcher()
    mock_trace = {
        "id": "test_001",
        "input": "Refund policy?",
        "output": "You get 100% refund anytime.",
        "error": ""
    }
    result = watcher.capture_failure(mock_trace)
    assert result["has_error"] is True
    assert result["incident_id"] == "test_001"

def test_auto_healer_timeout_trigger():
    healer = CockroachAutoHealer()
    error_log = "Error: connection pool exhausted timeout"
    result = healer.heal_database_issue(error_log)
    assert result["status"] == "SUCCESS"
