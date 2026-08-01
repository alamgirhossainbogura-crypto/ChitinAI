from chitin.main import run_chitin_pipeline

def monitor_my_agent(user_input: str, agent_output: str, error_log: str = ""):
    """
    Drop-in wrapper for external AI bts.
    Pass agent responses here to trigger autonomous self-healing.
    """
    trace_payload = {
        "id": "prod_trace_999",
        "input": user_input,
        "output": agent_output,
        "error": error_log
    }
    
    return run_chitin_pipeline(trace_payload)
