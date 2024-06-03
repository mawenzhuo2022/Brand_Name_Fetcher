import json
import os
import requests
from dotenv import load_dotenv
import openai

# 加载环境变量，包括OpenAI的API密钥
load_dotenv()
# 用API密钥初始化OpenAI客户端
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def extract_titles(json_path):
    """
    从指定的JSON文件中提取所有"title"字段。
    """
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    titles = [info['zh']['title'] for key, info in data.items() if 'zh' in info and 'title' in info['zh']]
    return titles


def send_titles_to_gpt_api(titles, filename, system_prompt):
    """
    将提取的标题和文件名发送到GPT API进行处理，使用从文件读取的 system prompt。
    """
    filename_prefix = f"({filename.replace('.json', '')}) titles:\n"
    user_prompt_content = filename_prefix + ', '.join(titles)
    print("Sending the following content to the GPT API:", user_prompt_content)  # 打印即将发送的内容
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt_content}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content  # Corrected access to content
    except Exception as e:
        print(f"Error communicating with GPT API: {e}")
        return None


def main():
    directory_path = '../dat/fetched/'
    result_path = '../dat/titles/'

    system_prompt_path = '../dat/prompt/system_prompt.txt'

    # 从文件读取 system prompt
    with open(system_prompt_path, 'r', encoding='utf-8') as prompt_file:
        system_prompt = prompt_file.read()

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            json_path = os.path.join(directory_path, filename)
            try:
                titles = extract_titles(json_path)
                # 发送标题和文件名到GPT API并接收处理后的内容，使用从文件读取的 system prompt
                api_response = send_titles_to_gpt_api(titles, filename, system_prompt)
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
