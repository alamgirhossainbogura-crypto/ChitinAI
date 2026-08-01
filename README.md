# 🛡️ ChitinAI — Autonomous Self-Healing Supervisor Meta-Agent

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-brightgreen)](https://www.python.org/)
[![CI/CD Gate](https://github.com/alamgirhossainbogura-crypto/ChitinAI/actions/workflows/chitin-gate.yml/badge.svg)](https://github.com/alamgirhossainbogura-crypto/ChitinAI/actions)

> **"Agents fail quietly. ChitinAI catches, patches, and auto-heals them."**

ChitinAI is an enterprise-grade meta-agent that monitors live LLM agents, catches prompt hallucinations, executes infrastructure auto-healing via CockroachDB, and optimizes model inference routing through AWS Bedrock.

---

## 📐 Architecture & Data Flow

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
## 🏛️ System Components

* **🔍 Watcher:** Real-time trace scanner and fault detector (`chitin/watcher.py`)
* **🧠 Vector Memory:** CockroachDB Distributed Vector Search & Bedrock Titan (`chitin/memory/crdb_vector.py`)
* **⚙️ Auto-Healer:** Database CLI engine for infrastructure auto-scaling (`chitin/memory/ccloud_cli.py`)
* **⚡ Cost Optimizer:** Dynamic model router switching between Claude 3.5 Sonnet & Amazon Nova (`chitin/llm/aws_bedrock.py`)
* **📊 Visual Cockpit:** React / Vite Prompt Diff & Live Replay UI (`dashboard/`)

---

## ⚡ Quick Start

### 1. Clone & Install

# Clone the repository
git clone [https://github.com/alamgirhossainbogura-crypto/ChitinAI.git](https://github.com/alamgirhossainbogura-crypto/ChitinAI.git)
cd ChitinAI

# Install Python dependencies
pip install -r requirements.txt

### 2. Run Backend Pipeline
python chitin/main.py

### 3. Launch Visual Cockpit
