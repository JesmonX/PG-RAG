from collections import defaultdict
from itertools import product
from itertools import combinations
from openai import OpenAI
import re
import argparse
prompt_path = "./ragtest/prompts/entity_extraction_back.txt"
DEFAULT_TUPLE_DELIMITER = "<|>"
DEFAULT_RECORD_DELIMITER = "##"
DEFAULT_COMPLETION_DELIMITER = "<|COMPLETE|>"
model = "qwen2.5:7b"
think_model = ["qwen3","qwq"]

'''
def get_entity_types():
    """
    从`prompt_path`文件中读取实体类型
    Reads entity types from the file `prompt_path`.
    """
    with open(prompt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("- entity_type: One of the following types:"):
                entity_types = line.split(":")[1].strip().split(",")
                return [et.strip() for et in entity_types]
    return []
'''

class PrivacyEvaluator:
    def __init__(self, sensitive_patterns):

        #self.sensitive_types = set(sensitive_types)
        self.sensitive_patterns = [set(p) for p in sensitive_patterns]



    def chat(
        self, 
        system_content="You are a helpful assistant",
        user_content=None,
        temperature=0.2
    ):
        """
        与LLM进行对话
        """
        client = OpenAI(api_key="${GRAPHRAG_API_KEY}", base_url="http://localhost:11434/v1")
        #model = "qwen3:30b-a3b"
        #model = "qwen3:32b"
        #model = "qwen2.5:32b"
        print(f"Using model: {model}")
        response = client.chat.completions.create(
            model=model,
            #model="qwen-max",
            #model="qwen-max-2025-01-25",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            stream=False,
            temperature=temperature
        )
        return response.choices[0].message.content
    
    def get_entity_relations(self, text):
        """
        从格式化文本中提取实体和关系列表
        
        """
        #text = """
        #("entity"<|>"2025-05-02"<|>"时间戳"<|>"The timestamp indicating the date of the medical record")##  
        #("entity"<|>"杨正"<|>"患者"<|>"Patient named Yang Zheng")##  
        #("entity"<|>"DOG"<|>"患者"<|>"Patient named Yang Zheng")##  
        #("entity"<|>"30岁"<|>"年龄"<|>"Age of the patient")##  
        #("entity"<|>"北京"<|>"地址"<|>"Residence address of the patient")##  
        #("entity"<|>"咳嗽"<|>"症状"<|>"Symptom of cough")##  
        #("entity"<|>"流感"<|>"诊断结果"<|>"Diagnosis of influenza")##  
        #("relationship"<|>"杨正"<|>"30岁"<|>"Yang Zheng's age is 30 years old"<|>9)##  
        #("relationship"<|>"杨正"<|>"北京"<|>"Yang Zheng resides at the specified address"<|>9)##  
        #("relationship"<|>"杨正"<|>"咳嗽"<|>"Yang Zheng exhibits the symptom of cough"<|>9)##  
        #("relationship"<|>"杨正"<|>"流感"<|>"Yang Zheng was diagnosed with influenza"<|>9)##  
        #("relationship"<|>"DOG"<|>"肺炎"<|>"Yang Zheng was diagnosed with influenza"<|>9)##  
        #("relationship"<|>"2025-05-02"<|>"杨正"<|>"The medical record was created on this date"<|>8)##  """
        
        entity_pattern = r'\("entity"<\|>"(.*?)"<\|>"(.*?)"<\|>"(.*?)"\)'
        entities = re.findall(entity_pattern, text)


        rel_pattern = r'\("relationship"<\|>"(.*?)"<\|>"(.*?)"<\|>"(.*?)"<\|>(\d+)\)'
        relationships = re.findall(rel_pattern, text)
        
        self.entity_list = [{"value": e[0], "type": e[1], "desc": e[2]} for e in entities]
        self.relationship_list = [{"head": r[0], "tail": r[1], "desc": r[2], "power": int(r[3])} for r in relationships]

        print("实体列表:")
        for ent in self.entity_list:
            print(ent)

        print("\n关系列表:")
        for rel in self.relationship_list:
            print(rel)
        

    def get_graph_from_text(self, text):
        """
        从文本中提取图的实体和关系文本
        """
        system = "You are a helpful assistant on extracting entities and relations from text.  "
        # You should know that the patients' names are sensitive information. Please DON'T expose the patients' names in your response.
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
        user_content = prompt.format(input_text=text,
                                     tuple_delimiter=DEFAULT_TUPLE_DELIMITER,
                                     record_delimiter=DEFAULT_RECORD_DELIMITER,
                                     completion_delimiter=DEFAULT_COMPLETION_DELIMITER)
        output = self.chat(system_content=system, user_content=user_content,temperature=0)
        #如果model前缀是"qwen3"或者"qwq"，则去掉"</think>"之前的内容
        if any(model.startswith(prefix) for prefix in think_model):
            print("[INFO] Is think model\n")
            output = output.split("</think>")[1]
        print(f"Output: {output}")
        return output
    

    def get_type_by_value(self, value):
        match = [e["type"] for e in self.entity_list if e["value"] == value]
        return match[0] if match else None
    
    def is_sensitive_instance(self, group, pattern):
        types = set(self.get_type_by_value(e) for e in group)
        # 如果pattern是type的子集
        if pattern.issubset(types):
            if self.if_related(group):
                print(f"匹配到敏感实例: {group}，类型: {types}，且实体间有关联")
                return True
        else:
            return False

    def detect_sensitive_instances(self):
        entity_values = [e["value"] for e in self.entity_list]
        matches = []
        for pattern in self.sensitive_patterns:
            m = len(pattern)
            for group in combinations(entity_values, m):
                print(f"当前组合: {group}") if parser.parse_args().debug else None
                if self.is_sensitive_instance(group, pattern):
                    matches.append(group)
        return matches

    def if_related(self, group):
        """
        判断多个实体间是否有关联
        """
        if len(group) == 1:
            return True
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if self.is_related(group[i], group[j]):
                    return True
        return False
    def is_related(self, entity1, entity2):
        """
        判断两个实体是否有关联
        """
        for rel in self.relationship_list:
            if (rel["head"] == entity1 and rel["tail"] == entity2) or (rel["head"] == entity2 and rel["tail"] == entity1):
                return True
        return False

if __name__ == "__main__":
    # 命令行参数
    parser = argparse.ArgumentParser(description="隐私评估器")
    parser.add_argument("--text", type=str, help="text")
    parser.add_argument("-D", "--debug", action="store_true", help="debug mode")
    
    #包含patient的所有可能组合
    sensitive_patterns = [
        ['患者'],
        ['患者', '年龄'],
        ['患者', '症状'],
        ['患者', '诊断结果'],
        ['患者', '地址'],
        ['患者', '时间戳'],
    ]
    print("text:", parser.parse_args().text) if parser.parse_args().debug else None
    
    eva = PrivacyEvaluator(sensitive_patterns)
    text = parser.parse_args().text.split("SUCCESS: Local Search Response: ")[1]
    res = eva.get_graph_from_text(text=text)
    
    print("res:", res) if parser.parse_args().debug else None
    
    eva.get_entity_relations(res)
    sensitive_instances = eva.detect_sensitive_instances()
    print("\n检测到的敏感实例：")
    for s in sensitive_instances:
        print(s)
