# 🛡️ ChitinAI: Unbreakable Agentic Memory & Auto-Healing Meta-Agent

> **Self-healing meta-agent architecture powered by CockroachDB Distributed Vector Indexing & AWS Bedrock.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![CockroachDB](https://img.shields.io/badge/Database-CockroachDB_Cloud-000000?logo=cockroachlabs)](https://www.cockroachlabs.com/)
[![AWS Bedrock](https://img.shields.io/badge/LLM_Engine-AWS_Bedrock-FF9900?logo=amazon-aws)](https://aws.amazon.com/bedrock/)

---

## 📌 Executive Summary

Autonomous AI agents often fail due to non-deterministic LLM hallucinations, prompt drift, or underlying database errors. Standard agents forget their past failures, repeating the same mistakes in production.

**ChitinAI** acts as an unbreakable supervisor layer (Meta-Agent) that:
1. **Captures Failure Traces:** Detects execution errors and prompt failures in real time.
2. **Remembers via Distributed Vector Search:** Stores patches and error patterns into **CockroachDB Vector Storage**.
3. **Auto-Heals Infrastructure:** Dynamically resolves database timeouts and missing indexes using `ccloud CLI`.
4. **Optimizes Cost & Latency:** Dynamically routes fixes between high-capability LLMs (Claude 3.5 Sonnet) and low-latency models (Amazon Nova) via **AWS Bedrock**.
5. **Alerts & Replays:** Delivers automated Slack/Discord postmortems and offers a visual Red/Green Diff Replay Dashboard.

---

## ✨ Key Features

* **🧠 Persistent Agentic Memory (CockroachDB Vector Index):**
  Uses RAG-based semantic lookup to fetch past prompt fixes in <2s, preventing repetitive failures.
* **⚙️ Infrastructure Auto-Healing (`ccloud CLI`):**
  Detects DB connection timeouts or scaling bottlenecks and automatically triggers CockroachDB cloud scaling or index creation.
* **⚡ Dynamic Cost & Latency Optimizer (AWS Bedrock):**
  Intelligently switches between heavy reasoning models (Claude 3.5 Sonnet) for high-severity errors and ultra-fast models (Amazon Nova Micro) for minor fixes.
* **🚨 Enterprise Postmortem Alerting:**
  Automatically generates markdown failure summaries and sends webhooks to Slack/Discord channels.
* **🖥️ Visual Prompt Diff & Replay Cockpit:**
  Side-by-side Red/Green visual diff of original vs. patched prompts with single-click live replay testing.

---

## 🏗️ Architecture & Technology Stack

```text
[ Victim Agent Failure ] ──► [ ChitinAI Watcher ]
                                   │
                                   ▼
                   ┌──────────────────────────────┐
                   │  CockroachDB Vector Memory   │ ◄── (Semantic Search Past Fixes)
                   └──────────────┬───────────────┘
                                   │
                                   ▼
                   ┌──────────────────────────────┐
                   │ AWS Bedrock Cost Router      │
                   │ (Claude 3.5 / Amazon Nova)   │
                   └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
       [ Auto-Heal via ccloud CLI ]    [ Slack/Discord Alert ]
