#!/bin/bash
# use: ./query.sh <method> <query> 
# method: local or global
# 将所有的参数都使用空格拼接到一起
query=$2
for arg in "${@:3}"
do
    query=$query\ $arg
done
#query=\"$query\"

printf "$query"
python -m graphrag.query --root ./ragtest --method $1 "$query"
