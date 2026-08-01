import os
import logging
from chitin.watcher import AgentWatcher
from chitin.memory.crdb_vector import CockroachVectorMemory
from chitin.memory.ccloud_cli import CockroachAutoHealer
from chitin.llm.aws_bedrock import BedrockCostOptimizer
from chitin.utils.notifier import IncidentNotifier

def run_chitin_pipeline(sample_trace: dict):
    logging.basicConfig(level=logging.INFO)
    logging.info("🛡️ Starting ChitinAI Meta-Agent Pipeline...")

    # Step 1: Watcher Captures Failure
    watcher = AgentWatcher()
    incident = watcher.capture_failure(sample_trace)

    if not incident["has_error"]:
        logging.info("✅ No agent errors or hallucinations detected.")
        return {"status": "HEALTHY"}

    # Step 2: Check Vector Memory (RAG Lookup)
    memory = CockroachVectorMemory()
    existing_fix = memory.search_similar_fix(incident["input"])

    if existing_fix:
        logging.info("🧠 [Memory Hit] Found existing patch in CockroachDB Vector Index!")
        return {"status": "RESOLVED_FROM_MEMORY", "patch": existing_fix["patched_prompt"]}

    # Step 3: Infrastructure Auto-Healing
    healer = CockroachAutoHealer()
    infra_status = healer.heal_database_issue(incident["error_log"])

    # Step 4: AWS Bedrock LLM Patch Generation
    optimizer = BedrockCostOptimizer()
    prompt_to_fix = f"Fix system prompt for failed input: {incident['input']} where agent gave bad output: {incident['output']}"
    llm_res = optimizer.generate_fix(prompt_to_fix, severity=incident["severity"])

    # Step 5: Save Patch to CockroachDB
    memory.store_fix(
        incident_id=incident["incident_id"],
        failure_type="Hallucination/Execution Error",
        failing_input=incident["input"],
        patched_prompt=llm_res["response"]
    )

    # Step 6: Dispatch Alert
    notifier = IncidentNotifier()
    notifier.send_postmortem(
        incident_id=incident["incident_id"],
        failure_type="Agent Execution Failure",
        model_used=llm_res["model_used"],
        fix_summary=llm_res["response"][:200]
    )

    return {
        "status": "AUTO_HEALED_AND_PATCHED",
        "model_used": llm_res["model_used"],
        "infra_action": infra_status,
        "patch": llm_res["response"]
    }

if __name__ == "__main__":
    # Test Run
    mock_failing_trace = {
        "id": "inc_101",
        "input": "What is the return policy for electronics?",
        "output": "You can return electronics anytime within 5 years for full cash refund.", # Hallucination
        "error": ""
    }
    result = run_chitin_pipeline(mock_failing_trace)
    print("\nPipeline Execution Result:\n", result)
