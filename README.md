# ZURU_company_assistant
This is a company assistant specially designed for ZURU.

## Architecture Overview
| Component                 | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| CLI Interface             | User interaction layer (input/output handling)                             |
| Query Classifier          | Determines query type (company/internal, general, ambiguous, restricted)   |
| Knowledge Base Retriever  | Extracts relevant info from local Markdown files (company docs)            |
| External Search Module    | Uses OpenRouter API + web search for general/up-to-date info               |
| Compliance Filter         | Blocks harmful or restricted queries           |
| Response Generator        | Synthesizes answers from appropriate sources (KB, search)       |

## Workflow
1. User inputs query via CLI
2. Compliance Filter first checks for restricted content (blocks if violated)
3. Query Classifier categorizes the query type
    a. Company query: Fetch from local KB
    b. General query: Use OpenRouter API + web search   
    c. Ambiguous query: Prompt user for clarification
4. Knowledge Base Retriever / External Search Module executes (based on query type)
5. Response Generator formats and returns the answer
6. CLI displays the response (with source attribution)

## Design Rationale
1. Modular Design: Separated components for maintainability
2. Local KB First: Prioritizes company docs for internal queries (reduces API costs + ensures accuracy)
3. Compliance First: Filters restricted and harmful queries before any processing
4. RAG applied: Combines retrieved context with LLM generation for better accuracy and relevance
5. Real-time search: retrieal from ZURU official website for up-to-date information (for company-related queries) if not found in KB
6. Fallback mechanism: If both KB and real-time search cannot answer the question, change the query type to general question and perform a general knowledge search to try to answer the question.
7. Cost Efficiency:
    a. Use lightweight model (Sentence-BERT) for KB retrieval (cheaper than LLM calls)
    b. Rate-limiting for OpenRouter API and SerpAPI to prevent overspending


## Setup Instructions
### Prerequisites
- Python 3.11
- OpenRouter API key

### Step 1: Clone Repository
git clone https://github.com/vfph55/ZURU_company_assistant.git
cd ZURU_company_assistant

### Step 2: Create Virtual Environment
conda create -n zuru python=3.11
conda activate zuru

### Step 3: Install Dependencies
pip install -r requirements.txt

### Step 4: Configure Environment Variables
Fill your own OpenRouter API in .env file

### Step 5: Run the Assistant
python src/main.py

## Code Structure
ZURU_company_assistant/
├── .env                        # environment variables
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies
├── knowledge_base/             # Company Markdown files
│   ├── Company Policies.md
│   ├── Coding Style.md
│   └── Company Procedures & Guidelines.md
└── src/
    ├── __init__.py
    ├── main.py                 # CLI entry point
    ├── agent/                  # Core agent logic
    │   ├── __init__.py
    │   ├── query_classifier.py # Query type detection
    │   ├── kb_retriever.py     # Local KB retrieval
    │   ├── external_search.py  # OpenRouter + web search
    │   ├── compliance_filter.py # Harmful content filtering
    │   └── response_generator.py # Answer synthesis
    ├── utils/                  # Helper functions
    │   ├── __init__.py
    │   ├── markdown_parser.py  # Parse Markdown files
    │   ├── env_loader.py       # Load environment variables
    │   └── logger.py           # Logging utility
    └── config/                 # Configuration
        ├── __init__.py
        └── settings.py         # App settings