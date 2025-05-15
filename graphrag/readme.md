
## 需要conda activate gr 和 ollama serve(如果address already in use就是已经开了)
## graphrag index构建
将input的txt复制到graphrag/ragtest/preinput
```
bash index.sh
```
如果数据不是类似`患者,年龄,地址,症状,诊断结果`的内容，则需要取消`index.sh`中`#python -m graphrag.prompt_tune --root ./ragtest/`的注释，以重新构建提示词。
## graphrag query
```
bash query.sh global/local 问题内容
```
## 其他
可以在graphrag/ragtest/settings.yaml中更改LLM和emb model。
