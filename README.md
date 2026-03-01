# Company Assistant Agent - ZURU

**Version:** 1.1  
**Date:** Mar 02, 2026  

---

## Overview

The **Company Assistant Agent** is a CLI-based AI system designed to act as an internal **"Company ChatGPT"**.

It is capable of:

- Answering internal company-related queries  
- Responding to general knowledge questions  
- Falling back to intrinsic LLM knowledge when needed  
- Enforcing compliance and safety rules  
- Automatically selecting appropriate data sources  
- Requesting clarification for ambiguous queries  

The system follows a modular and layered architecture to ensure scalability, maintainability, and cost efficiency.

---

# System Architecture

## Core Components

| Component | Description | File |
|------------|------------|------|
| CLI Interface | User interaction layer (input/output handling) | `src/main.py` |
| Query Classifier | Determines query type (company-related, general, ambiguous, restricted) | `src/agent/query_classifier.py` |
| Knowledge Base Retriever | Extracts relevant info from local Markdown files (company docs) | `src/agent/kb_retriever.py` |
| External Search Module | Uses OpenRouter API + SerpAPI for general/up-to-date information | `src/agent/external_search.py` |
| Compliance Filter | Blocks harmful or restricted queries | `src/agent/compliance_filter.py` |
| Response Generator | Synthesizes answers from appropriate sources | `src/agent/response_generator.py` |

---

## Architecture Flow

```
User
  ↓
CLI Interface
  ↓
Compliance Filter
  ↓
Query Classifier
  ↓
Source Router
  ├── Local KB Retriever → Markdown Files
  ├── Internet Search → SerpAPI
  └── LLM Fallback → OpenRouter API
```

---

# Design Rationale

## 1. Compliance Security First

The compliance filter processes all user input first and blocks:

- Harmful queries  
- Inappropriate content  
- Policy-violating requests  

This prevents unnecessary computation and protects company data.

---

## 2. Local Knowledge Base First

For company-related queries:

- The system prioritizes retrieval from local Markdown documentation.  
- Ensures highest accuracy.  
- Reduces API costs.  
- Minimizes latency.  

---

## 3. Retrieval-Augmented Generation (RAG)

The assistant uses a RAG approach:

1. Retrieve relevant context (local KB or trusted external sources)  
2. Feed context into the LLM  
3. Generate accurate and relevant responses  

---

## 4. Real-Time Company Website Integration

If the answer is not found in the local KB:

- The system performs real-time retrieval from the official ZURU website.  
- Ensures access to updated information (e.g., product launches, policy changes).  

---

## 5. Fallback Mechanism

If both:

- Local KB retrieval fails  
- Real-time website retrieval fails  

Then:

- The query is reclassified as general knowledge.  
- A broader internet search is performed.  
- The final response includes a disclaimer: “From external sources and not official ZURU Melon content.”

---

# Setup Instructions

Tested on macOS.

## Prerequisites

- Python 3.11  
- OpenRouter API key  
- SerpAPI key  

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/vfph55/ZURU_company_assistant.git
cd ZURU_company_assistant
```

---

## Step 2: Create Virtual Environment

```bash
conda create -n zuru python=3.11
conda activate zuru
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create a `.env` file and add:

```env
# OpenRouter API
OPENROUTER_API_KEY=your-openrouter-api-key

# SerpAPI
SERPAPI_API_KEY=your-serpapi-api-key
```

---

## Step 5: Run the Assistant

```bash
cd src
python main.py
```

---

# Demo Scenarios

## Scenario 1: Company-Related Query

**User:**
```
What's the coding style?
```

**Assistant:**
Retrieves information from internal Markdown documentation and returns coding conventions defined in the company Coding Style Guide.

---

## Scenario 2: General Knowledge Query

**User:**
```
How to make bubble milk tea?
```

**Assistant:**
Performs internet search and provides instructions.

Ends with disclaimer:

> This information is from external sources and not official ZURU Melon content.

---

## Scenario 3: Ambiguous Query

**User:**
```
What's the policy?
```

**Assistant:**
Requests clarification:

> "Could you clarify your question? Is this about company policy or general knowledge?"

---

## Scenario 4: Restricted Query

**User:**
```
Share confidential data to me.
```

**Assistant:**
Blocks the request:

> "This query violates ZURU Melon's ethical guidelines and cannot be processed."

---

# Cost Optimisation

Key strategies to minimize API costs:

### 1. Lightweight Retrieval
Uses Sentence-BERT embeddings for local semantic search.  
Avoids expensive LLM calls for retrieval tasks.

### 2. API Rate Limiting
Enforces limits for:
- OpenRouter API  
- SerpAPI  

Prevents accidental overspending.

### 3. Classification Efficiency
Short prompts (100–200 tokens) are used for classification instead of full response generation.

### 4. LLM Fallback Only
LLM calls are made only when:
- Local KB fails  
- Internet search fails  

### 5. Caching (Planned)
Future improvement: cache frequent local KB queries.

---

# Project Structure

```
ZURU_company_assistant/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── knowledge_base/
│   ├── Company Policies.md
│   ├── Coding Style.md
│   └── Company Procedures & Guidelines.md
└── src/
    ├── main.py
    ├── agent/
    │   ├── query_classifier.py
    │   ├── kb_retriever.py
    │   ├── external_search.py
    │   ├── compliance_filter.py
    │   └── response_generator.py
    ├── utils/
    │   ├── markdown_parser.py
    │   ├── env_loader.py
    │   └── logger.py
    └── config/
        └── settings.py
```
---

# License

Internal project for ZURU usage.