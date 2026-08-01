# 🏗️ ChitinAI: Architecture & System Design

**ChitinAI** acts as an unbreakable supervisor layer (Meta-Agent) designed to monitor, auto-heal, and optimize autonomous LLM agent execution in production environments.

---

## 📐 System Architecture

Below is the execution flow of how ChitinAI captures agent failures, resolves database/prompt issues, and logs vector memory.

+-------------------+      +-------------------+      +-------------------------+
| Victim AI Agent   | ---> | ChitinAI Watcher  | ---> | CockroachDB Vector RAG  |
| (Failing Prompt)  |      | Trace Ingestion   |      | (Past Incident Search)  |
+-------------------+      +-------------------+      +-------------------------+
|
v
+-------------------+      +-------------------+      +-------------------------+
| Slack / Discord   | <--- | ccloud CLI        | <--- | AWS Bedrock Router      |
| Postmortem Alert  |      | Auto-Healer       |      | (Sonnet 3.5 / Nova)     |
+-------------------+      +-------------------+      +-------------------------+




---

## 🏛️ Key Subsystems & Components

### 1. 🔍 Agent Watcher (`chitin/watcher.py`)
* Monitors execution traces and output payloads in real time.
* Flags non-deterministic LLM hallucinations, schema violations, and database connectivity failures.

### 2. 🧠 Distributed Vector Memory (`chitin/memory/crdb_vector.py`)
* Powered by **CockroachDB Vector Search** and **AWS Bedrock Titan Embeddings**.
* Performs RAG-based lookup ($<2\text{s}$) to check if a similar error/hallucination has occurred before.
* Retrieves previously verified prompt patches to instantly resolve issues without triggering heavy reasoning loops.

### 3. ⚙️ Infrastructure Auto-Healer (`chitin/memory/ccloud_cli.py`)
* Intercepts database connection pool timeouts and missing index execution bottlenecks.
* Executes autonomous infrastructure scaling commands using the **`ccloud` CLI**.

### 4. ⚡ Dynamic Cost & Latency Optimizer (`chitin/llm/aws_bedrock.py`)
* Intelligent model router on **AWS Bedrock**:
  * **Claude 3.5 Sonnet:** Routed for `HIGH` / `CRITICAL` severity reasoning and complex prompt patches.
  * **Amazon Nova Micro:** Routed for `LOW` / `MEDIUM` severity errors to ensure ultra-low latency and reduced cost.

### 5. 🚨 Postmortem Webhook Alerting (`chitin/utils/notifier.py`)
* Generates markdown incident summaries and automatically dispatches webhooks to configured **Slack / Discord** channels.

---

## 🔄 Data Flow Sequence

1. **Failure Ingestion:** Production Agent triggers an error $\rightarrow$ Handled by `AgentWatcher`.
2. **Vector Retrieval:** `CockroachVectorMemory` executes similarity search.
   * *If match found:* Instantly returns cached prompt patch.
   * *If no match:* Proceeds to root-cause diagnosis.
3. **Infrastructure Check:** `CockroachAutoHealer` verifies DB health via `ccloud CLI`.
4. **LLM Patch Generation:** `BedrockCostOptimizer` generates a corrected prompt based on error severity.
5. **Persistence:** New patch + embedding vector is stored in CockroachDB.
6. **Notification:** Postmortem dispatched to team channels via `IncidentNotifier`.
