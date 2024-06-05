# -*- coding: utf-8 -*-
# @Author: Wenzhuo Ma
# @Time: 2024/6/4 13:28
# @Description: This script asynchronously processes CSV files by querying the OpenAI GPT API.
# It extracts non-empty titles from the second column of CSV files, sends each title to the GPT API,
# processes the returned synonyms, and saves the enriched data as JSON in a specified output directory.
# This approach is designed to efficiently handle large datasets and reduce processing time.

import csv
import json
import asyncio
import aiohttp
import os
from pathlib import Path
from dotenv import load_dotenv
import openai
import logging

# Configure logging to output timestamped messages at INFO level, aiding in debugging and system monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load API key from environment variable for security reasons
load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


async def send_title_to_gpt_api(session, title, filename, system_prompt, custom_prompt_suffixes):
    """
    Asynchronously sends a title to the OpenAI GPT API and processes the response.

    Args:
        session (aiohttp.ClientSession): Active session to handle HTTP requests.
        title (str): The title extracted from the CSV file.
        filename (str): The base name of the input file, used to customize prompts if necessary.
        system_prompt (str): The default prompt template for the GPT API call.
        custom_prompt_suffixes (dict): Optional suffixes to append to the system prompt based on filename.

    Returns:
        dict: A dictionary with processed synonyms if API call is successful; None if an error occurs.
    """
    if not title:
        logging.info("Skipping empty title.")
        return None

    filename_key = filename.replace('.json', '')
    custom_prompt = custom_prompt_suffixes.get(filename_key, "")
    full_system_prompt = system_prompt + custom_prompt
    user_prompt_content = f"({filename_key}) title:\n" + title

    logging.info(f"Sending '{title}' to GPT API using prompt: {user_prompt_content}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": user_prompt_content}
            ],
            temperature=0.6
        )
        content = response.choices[0].message.content.strip()
        synonyms = [line.strip() for line in content.split('\n') if line.strip()]
        logging.info(f"Received synonyms for '{title}'.")
        return {
            "metric_id": filename_key,
            "synonyms": synonyms,
            "display_name": "Default Display Name",
            "metadatas": {"cit": "Default CIT", "category": "Performance"}
        }
    except Exception as e:
        logging.error(f"Failed to process '{title}' with error: {e}")
        return None


async def process_csv_and_call_gpt(session, input_file, system_prompt, custom_prompt_suffixes):
    """
    Processes each CSV file, sending titles to the GPT API and compiling results.

    Args:
        session (aiohttp.ClientSession): Session object for making HTTP requests.
        input_file (str): Path to the CSV file to be processed.
        system_prompt (str): Default prompt for GPT API interaction.
        custom_prompt_suffixes (dict): Custom suffixes for prompts based on file specifics.

    Returns:
        List[dict]: List of dictionaries with the results from the GPT API for each title.
    """
    results = []
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header to start processing actual data
        for row in reader:
            if row and len(row) > 1 and row[1].strip():
                result = await send_title_to_gpt_api(session, row[1], input_file.stem, system_prompt,
                                                     custom_prompt_suffixes)
                if result:
                    results.append(result)

    logging.info(f"Completed processing '{input_file}'. Processed {len(results)} entries.")
    return results


async def process_all_csvs(input_dir, output_dir, system_prompt):
    """
    Initiates processing of all CSV files in a directory and saves results as JSON files.

    Args:
        input_dir (str): Directory containing the CSV files.
        output_dir (str): Directory where JSON results will be saved.
        system_prompt (str): Default GPT system prompt for generating responses.
    """
    async with aiohttp.ClientSession() as session:
        for input_file in Path(input_dir).glob('*.csv'):
            results = await process_csv_and_call_gpt(session, input_file, system_prompt, custom_prompt_suffixes={})
            output_file = Path(output_dir) / f"{input_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            logging.info(f"Output saved to '{output_file}'.")


async def main():
    """
    Main function to set up and execute the data processing tasks.
    """
    system_prompt_path = "../dat/prompt/system_prompt.txt"
    input_dir = "../dat/raw_data/"
    output_dir = "../dat/result/"
    with open(system_prompt_path, 'r', encoding='utf-8') as file:  # Specify encoding here
        system_prompt = file.read().strip()
    await process_all_csvs(input_dir, output_dir, system_prompt)


if __name__ == "__main__":
    asyncio.run(main())
