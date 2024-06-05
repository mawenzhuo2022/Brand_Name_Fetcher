# Similar Names Processor

## Description
This script is designed to process data from CSV files by querying the OpenAI GPT API. It reads each non-empty title from the second column of CSV files, sends it to the GPT API, and saves the enriched data in JSON format in a specified output directory. This automation enhances data sets with advanced AI capabilities, ideal for tasks requiring semantic analysis or data enrichment.

## Features
- Processes CSV files to extract titles.
- Integrates with OpenAI's GPT-3.5-turbo model for dynamic data processing.
- Saves enriched titles in a structured JSON format.
- Enterprise-grade logging for monitoring and debugging.

## System Requirements
- Python 3.8 or higher
- aiohttp
- python-dotenv
- OpenAI Python Client

## Installation

First, ensure Python and pip are installed on your system. Then, install the required packages using the following command:

```bash
pip install aiohttp python-dotenv openai
```

## Configuration
Before running the script, make sure to configure the following:

### Environment Variables:
- Create a `.env` file in the project's root directory.
- Add `OPENAI_API_KEY=<Your-OpenAI-API-Key>` to the `.env` file. Replace `<Your-OpenAI-API-Key>` with your actual OpenAI API key.

### Input/Output Directories:
- Ensure your CSV files are placed in `../dat/raw_data/`.
- Output files will be saved in `../dat/result/`.

## Usage
To run the script, navigate to the `src/similar_names` directory and execute the `main.py` script. Follow these steps:

```bash
cd src/similar_names
python main.py
```

## Author

- **Wenzhuo Ma** - Initial work and ongoing maintenance.

Feel free to contact me for any questions or feedback regarding this project.
