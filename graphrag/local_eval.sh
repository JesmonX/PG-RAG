#!/bin/bash
# use: ./query.sh <method> <query> 
# method: local or global
# 将所有的参数都使用空格拼接到一起
query=$1
for arg in "${@:2}"
do
    query=$query\ $arg
done
#query=\"$query\"

printf "$query"
python -m graphrag.query --root ./ragtest --method local "$query" > tmp.txt

python privacy.py --text "$(cat tmp.txt)"
