#{"text": "《邪少兵王》是冰火未央写的网络小说连载于旗峰天下", "spo_list": [{"predicate": "作者", "object_type": {"@value": "人物"}, "subject_type": "图书作品", "object": {"@value": "冰火未央"}, "subject": "邪少兵王"}]}

#只从json文件中读取text项，忽略其他所有
import json
import os
import re
import requests
file = 'ccks2017_task2.json'
#提取无后缀文件名
file_name = file.split('.')[0]
text = ""
i = 0
with open(file, 'r', encoding='utf-8') as f:
    with open(f'{file_name}.txt', 'w', encoding='utf-8') as f2:
        for line in f:
            i += 1
            print(i, end='\r')
            text = json.loads(line)['text'] + '\n'
            f2.write(text)
            if i == 10000:
                break

#with open('text.txt', 'w', encoding='utf-8') as f:
#    f.write(text)
    

