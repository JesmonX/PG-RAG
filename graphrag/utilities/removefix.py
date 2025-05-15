#对于 catch文件夹中的所有文件，删除‘**’符号（使用""替代"**"）
import os
import re
import shutil
import sys

def remove_double_star_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove '**' from the content
    modified_content = re.sub(r'\*\*', '', content)

    with open(file_path, 'w') as file:
        file.write(modified_content)
        print(f"Processed file: {file_path}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            remove_double_star_from_file(file_path)

if __name__ == "__main__":
    # Specify the directory to process
    directory_to_process = '/amax/home/yanzheng/graphrag/ragtest/cache/entity_extraction'    
    # Check if the directory exists
    if os.path.exists(directory_to_process):
        process_directory(directory_to_process)
    else:
        print(f"Directory '{directory_to_process}' does not exist.")