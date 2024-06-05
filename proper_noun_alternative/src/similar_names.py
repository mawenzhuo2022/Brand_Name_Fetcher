# -*- coding: utf-8 -*-
# @Author: Wenzhuo Ma
# @Time: 2024/6/4 13:28
# @Description: This script processes data from CSV files by querying the OpenAI GPT API.
# It reads each non-empty title from the second column of CSV files, sends it to the GPT API,
# and then saves the enriched data as JSON format in the specified output directory.

import csv
import json
import asyncio
import aiohttp
import os
from pathlib import Path
from dotenv import load_dotenv
import openai
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


async def send_title_to_gpt_api(session, title, filename, system_prompt, custom_prompt_suffixes):
    """Sends individual title to the GPT API and returns the processed response.

    Args:
        session (ClientSession): The aiohttp session.
        title (str): The title to process.
        filename (str): The filename used to determine the prompt customization.
        system_prompt (str): Base system prompt for GPT.
        custom_prompt_suffixes (dict): Contains custom suffixes for system prompts.

    Returns:
        dict: A dictionary with the original title as key and the list of processed titles as value.
    """
    if not title:
        logging.info(f"Skipping empty title.")
        return None

    filename_key = filename.replace('.json', '')
    custom_prompt = custom_prompt_suffixes.get(filename_key, "")
    full_system_prompt = system_prompt + custom_prompt
    user_prompt_content = f"({filename_key}) title:\n" + title

    logging.info(f"Sending to GPT API: {user_prompt_content}")

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
        split_content = [line.strip() for line in content.split('\n') if line.strip()]
        logging.info(f"Received processed content for '{title}'.")
        return {title: split_content}
    except Exception as e:
        logging.error(f"Error communicating with GPT API for title '{title}': {e}")
        return {title: None}


async def process_csv_and_call_gpt(session, input_file, system_prompt, custom_prompt_suffixes):
    """Processes each CSV file, sends each title to the GPT API, and gathers results.

    Args:
        session (ClientSession): The aiohttp session.
        input_file (str): Path to the input CSV file.
        system_prompt (str): Base system prompt for GPT.
        custom_prompt_suffixes (dict): Contains custom suffixes for system prompts.
    """
    tasks = []
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            if row and len(row) > 1 and row[1].strip():
                task = send_title_to_gpt_api(session, row[1], input_file.stem + '.json', system_prompt,
                                             custom_prompt_suffixes)
                tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)
    data = {}
    for result in results:
        if result:
            data.update(result)

    logging.info(f"Processed file '{input_file}' with {len(tasks)} titles.")
    return data


async def process_all_csvs(input_dir, output_dir, system_prompt):
    """Processes all CSV files in the given directory and saves the results as JSON files.

    Args:
        input_dir (str): Directory containing CSV files.
        output_dir (str): Directory to save output JSON files.
        system_prompt (str): Base system prompt for GPT.
    """
    custom_prompt_suffixes = {}
    async with aiohttp.ClientSession() as session:
        for input_file in Path(input_dir).glob('*.csv'):
            data = await process_csv_and_call_gpt(session, input_file, system_prompt, custom_prompt_suffixes)
            output_file = Path(output_dir) / (input_file.stem + ".json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"Saved JSON file: {output_file}")


async def main():
    """Main function to setup and run the processing tasks."""
    system_prompt_path = "../dat/prompt/system_prompt.txt"
    input_dir = "../dat/raw_data/"
    output_dir = "../dat/result/"
    with open(system_prompt_path, 'r') as file:
        system_prompt = file.read().strip()
    await process_all_csvs(input_dir, output_dir, system_prompt)


if __name__ == "__main__":
    asyncio.run(main())
