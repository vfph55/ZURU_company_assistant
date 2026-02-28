# ZURU_company_assistant
This is a company assistant specially designed for ZURU.

## architecture overview
| Component                 | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| CLI Interface             | User interaction layer (input/output handling)                             |
| Query Classifier          | Determines query type (company/internal, general, ambiguous, restricted)   |
| Knowledge Base Retriever  | Extracts relevant info from local Markdown files (company docs)            |
| External Search Module    | Uses OpenRouter API + web search for general/up-to-date info               |
| Security Filter         | Blocks harmful or restricted queries           |
| Response Generator        | Synthesizes answers from appropriate sources (KB, search)       |


## environment setup
conda create -n zuru python=3.11