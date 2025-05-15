#!/bin/bash
mv ragtest/output/* ragtest/preoutput/ #备份原本的输出
rm -r ./ragtest/input/* #删除原本的分块输入
rm -r ./ragtest/cache/* #删除缓存
python utilities/split.py $1 1    #按换行符分块
#python -m graphrag.prompt_tune --root ./ragtest/
python -m graphrag.index --root ./ragtest #第一次构建
#python utilities/removefix.py #如果出错，修改缓存的内容
#python -m graphrag.index --root ./ragtest #第二次构建（如果第一次构建成功，那么这次构建就是走个形式）


