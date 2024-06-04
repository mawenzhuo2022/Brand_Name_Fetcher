import json
import os
import requests
from dotenv import load_dotenv
import openai

load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_titles(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    titles = [info['zh']['title'] for key, info in data.items() if 'zh' in info and 'title' in info['zh']]
    return titles

def send_titles_to_gpt_api(titles, filename, system_prompt, custom_prompt_suffixes):
    filename_key = filename.replace('.json', '')
    # 从字典中获取对应的prompt后缀
    custom_prompt = custom_prompt_suffixes.get(filename_key, "")
    # 将自定义prompt添加到系统prompt之后
    full_system_prompt = system_prompt + custom_prompt

    filename_prefix = f"({filename_key}) titles:\n"
    user_prompt_content = filename_prefix + ', '.join(titles)
    print("Sending the following content to the GPT API:", user_prompt_content)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": user_prompt_content}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with GPT API: {e}")
        return None

def main():
    directory_path = '../dat/fetched/'
    result_path = '../dat/titles/'
    system_prompt_path = '../dat/prompt/system_prompt.txt'

    # 加载自定义prompt后缀
    custom_prompt_suffixes = {
        'Cisco': " Based on the request above, don't include the following '苹果', '联想集团', 'LG集团'",
        'H3C': " Based on the request above, don't include the following '苹果', '联想集团', 'LG集团'",
        'HP': " Based on the request above, don't include the following '苹果', '联想集团', 'LG集团'",
        'Huawei': " Based on the request above, don't include the following '苹果', '联想集团', 'LG集团'",
        'Microsoft': " Based on the request above, don't include the following '苹果', '联想集团', 'LG集团'",
    }

    with open(system_prompt_path, 'r', encoding='utf-8') as prompt_file:
        system_prompt = prompt_file.read()

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            json_path = os.path.join(directory_path, filename)
            try:
                titles = extract_titles(json_path)
                api_response = send_titles_to_gpt_api(titles, filename, system_prompt, custom_prompt_suffixes)
                if api_response:
                    output_path = os.path.join(result_path, filename.replace('.json', '_processed.txt'))
                    with open(output_path, 'w', encoding='utf-8') as file:
                        file.write(api_response)
                    print(f"Processed content from {filename} has been successfully written to {output_path}")
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")
            except Exception as e:
                print(f"An error occurred with {filename}: {e}")

if __name__ == '__main__':
    main()
