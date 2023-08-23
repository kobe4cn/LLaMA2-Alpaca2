import pandas as pd

# 读取Excel文件
excel_file = 'LRL种草贴数据.xlsx'
df = pd.read_excel(excel_file)

# 拆分数据并保存为多个CSV文件
batch_size = 500
num_files = (len(df) - 1) // batch_size + 1
for i in range(num_files):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, len(df))
    batch_df = df.iloc[start_idx:end_idx]

    # 生成文件名
    output_file = f'output_{i + 1}.xlsx'

    # 将DataFrame保存为CSV文件
    batch_df.to_excel(output_file, index=False)

print(f'{num_files}个文件已成功拆分和保存。')
