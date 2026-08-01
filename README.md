# 🛡️ ChitinAI — Autonomous Self-Healing Supervisor Meta-Agent

> **Agents fail quietly. ChitinAI catches, patches, and auto-heals them.**

ChitinAI is an enterprise-grade meta-agent that monitors live LLM agents, catches prompt hallucinations, executes infrastructure auto-healing via CockroachDB, and optimizes model inference routing through AWS Bedrock.

---

## 🏛️ System Architecture

- **Watcher:** Real-time trace scanner and fault detector (`chitin/watcher.py`)
- **Vector Memory:** CockroachDB Distributed Vector Search & Bedrock Titan (`chitin/memory/crdb_vector.py`)
- **Auto-Healer:** Database CLI engine for infrastructure auto-scaling (`chitin/memory/ccloud_cli.py`)
- **Cost Optimizer:** AWS Bedrock dynamic model router (`chitin/llm/aws_bedrock.py`)
- **Visual Cockpit:** React / Vite Prompt Diff & Replay UI (`dashboard/`)

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone [https://github.com/alamgirhossainbogura-crypto/ChitinAI.git](https://github.com/alamgirhossainbogura-crypto/ChitinAI.git)
cd ChitinAI

# Install dependencies
pip install -r requirements.txt

# Run backend pipeline
python chitin/main.py

# Launch frontend cockpit
cd dashboard
npm install
npm run dev
