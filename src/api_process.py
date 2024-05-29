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

def send_titles_to_gpt_api(titles):
    """
    将提取的标题发送到GPT API进行处理。
    """
    system_prompt_content = "Analyze the following titles and provide insights."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt_content},
                {"role": "user", "content": ', '.join(titles)}
            ],
            temperature=0.3
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error communicating with GPT API: {e}")
        return None

def main():
    directory_path = '../dat/results/'
    output_directory_path = '../dat/titles/'

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            json_path = os.path.join(directory_path, filename)
            try:
                titles = extract_titles(json_path)
                # 发送标题到GPT API并接收处理后的内容
                api_response = send_titles_to_gpt_api(titles)
                if api_response:
                    output_path = os.path.join(output_directory_path, filename.replace('.json', '_processed.txt'))
                    with open(output_path, 'w', encoding='utf-8') as file:
                        file.write(api_response)
                    print(f"Processed content from {filename} has been successfully written to {output_path}")
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")
            except Exception as e:
                print(f"An error occurred with {filename}: {e}")

if __name__ == '__main__':
    main()
