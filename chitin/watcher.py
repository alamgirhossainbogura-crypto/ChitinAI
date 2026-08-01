import logging

class AgentWatcher:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def capture_failure(self, agent_trace: dict) -> dict:
        """
        ইনকামিং ট্রেস থেকে ভুল সনাক্ত করা
        """
        error_message = agent_trace.get("error", "")
        input_text = agent_trace.get("input", "")
        output_text = agent_trace.get("output", "")

        logging.info(f"🔍 [Watcher] Scanning trace ID: {agent_trace.get('id', 'N/A')}")

        return {
            "incident_id": agent_trace.get("id", "inc_001"),
            "has_error": bool(error_message or "hallucination" in output_text.lower()),
            "input": input_text,
            "output": output_text,
            "error_log": error_message,
            "severity": "HIGH" if error_message else "LOW"
        }
