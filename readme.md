# Brand Name Fetcher

## Overview

The Brand Name Fetcher is a comprehensive suite consisting of two major components designed to enhance data processing
and web crawling capabilities:

1. **proper_noun_alternative** - This module focuses on processing data from CSV files to extract and analyze proper
   nouns, enhancing them with semantic data to create useful metadata representations.
2. **web_crawler** - This module is designed to scrape web pages for proprietary nouns and terms, enriching this data
   through AI-driven analysis to determine relevance and associations.

## Installation

Ensure Python 3.8 or higher is installed on your system. Both components require different dependencies, so refer to
each module's specific installation instructions below.

## Usage

Each module has specific usage instructions. Navigate to the respective module directory and follow the README.md
instructions for running the scripts.

## Components

### proper_noun_alternative

This component extracts titles from CSV files, processes them through OpenAI's GPT models, and outputs enhanced data in
JSON format.

#### Features

- Extracts data from CSV files efficiently.
- Utilizes AI for semantic analysis and enrichment.
- Outputs data in an easy-to-use JSON format.

#### System Requirements

- Python 3.8 or higher
- aiohttp
- python-dotenv
- OpenAI Python Client

#### Installation

```bash
pip install requests beautifulsoup4 spacy aiohttp python-dotenv openai
```

Additionally, download the required spaCy language model:

```bash
python -m spacy download en_core_web_sm
```

#### Configuration

Create a `.env` file in the project root directory:

```plaintext
OPENAI_API_KEY=<Your-OpenAI-API-Key>
```

## Author

- **Wenzhuo Ma** - Initial work and ongoing maintenance.

Feel free to contact me for any questions or feedback regarding this project.