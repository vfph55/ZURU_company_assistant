# ZURU_company_assistant
This is a company assistant specially designed for ZURU.

## overview
| Component                 | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| CLI Interface             | User interaction layer (input/output handling)                             |
| Query Classifier          | Determines query type (company/internal, general, ambiguous, restricted)   |
| Knowledge Base Retriever  | Extracts relevant info from local Markdown files (company docs)            |
| External Search Module    | Uses OpenRouter API + web search for general/up-to-date info               |
| Compliance Filter         | Blocks harmful/policy-violating queries per ZURU Melon guidelines          |
| Response Generator        | Synthesizes answers from appropriate sources (KB, search, intrinsic)       |


## environment setup
conda create -n zuru python=3.11