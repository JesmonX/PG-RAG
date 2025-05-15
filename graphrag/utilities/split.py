import os
import sys

def integrate_files(input_folder, output_file):
    """
    将文件夹中的所有文件合并为一个文件
    
    参数:
        input_folder: 输入的文件夹路径
        output_file: 输出的文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):  # 只处理文本文件
                with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # 添加换行符分隔不同文件的内容

def create_files_from_lines(input_file, output_folder=None, file_prefix='line_', file_extension='.txt'):
    """
    将文本文件的每一行创建为一个新文件
    
    参数:
        input_file: 输入的文本文件路径
        output_folder: 输出文件夹路径(可选，默认为当前目录)
        file_prefix: 生成文件的前缀(可选)
        file_extension: 生成文件的扩展名(可选)
    """
    # # 确保输出文件夹存在
    # if output_folder and not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    line_num = 0
    # 为每一行创建文件
    for i, line in enumerate(lines, start=1):
        # 去除行尾的换行符
        line_content = line.strip()
        
        # 生成文件名
        filename = f"{file_prefix}{i}{file_extension}"
        
        # 确定完整输出路径
        if output_folder:
            filepath = os.path.join(output_folder, filename)
        else:
            filepath = filename
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(line_content)
        line_num = i 
        
    print(f"已创建 {line_num} 个文件")
    

# 使用示例
if __name__ == "__main__":
    
    #path = "./ragtest/input"
    #name = "data_low_2.txt"
    num = 0
    # 接受命令行参数
    if len(sys.argv) > 1:
        #path = sys.argv[2]
        name = sys.argv[1]
        num = int(sys.argv[2])
    
    if num == 0:
        # 合并文件
        integrate_files('./ragtest/input', name)
    else:
        # 创建文件
        create_files_from_lines(name, './ragtest/input')