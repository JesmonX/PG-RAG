import yaml

with open('/amax/home/yanzheng/graphrag/ragtest/settings.yaml', 'r', encoding='utf-8') as f:
    result = yaml.load(f.read(), Loader=yaml.FullLoader)

prompt_path = '/amax/home/yanzheng/graphrag/ragtest/prompts/entity_extraction.txt'

def get_entity_types():
    """
    从文件中读取实体类型
    """
    with open(prompt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            
            if line.startswith("- entity_type: One of the following types:"):
                print(line)
                entity_types = line.split("types:")[1].strip().split(",")
                return [et.strip() for et in entity_types]
    return []

print(get_entity_types())
