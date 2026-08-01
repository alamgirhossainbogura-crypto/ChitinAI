# 📄 Product Requirements Document (PRD) - ChitinAI

## 1. Objective
Build an autonomous supervisor layer that intercepts failing LLM prompts and database timeouts without human intervention.

## 2. Core Functional Requirements
- **FR-1:** Automatic RAG search in CockroachDB Vector Memory ($<2\text{s}$ latency).
- **FR-2:** Dynamic Bedrock routing (Claude 3.5 Sonnet vs. Amazon Nova Micro).
- **FR-3:** Interactive Visual Diff dashboard for live prompt replays.
