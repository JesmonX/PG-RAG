import pandas as pd

# 读取Parquet文件
file_path = '/amax/home/yanzheng/graphrag/ragtest/output/20250407-211749-disease2/artifacts/create_base_documents.parquet'
file_name = file_path.split('/')[-1].split('.')[0]
print(f"File name: {file_name}")
csv_file_path = f"{file_name}.csv"
df = pd.read_parquet(file_path, engine='pyarrow')  # 或 engine='fastparquet'

# 保存为CSV文件
df.to_csv(csv_file_path, index=False)
