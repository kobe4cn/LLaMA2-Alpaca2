import pandas as pd
import requests
import os

def process_excel_with_api(input_file, output_file, api_url, column_to_process,headers):
    # 读取Excel文件
    print("input_file: "+ input_file)
    df = pd.read_excel(input_file)

    # 创建一个空列表用于保存处理结果
    results = []

    # 遍历每行数据
    for index, row in df.iterrows():
        # 获取当前行的需要处理的数据
        data_to_process = row[column_to_process]
        print(data_to_process)

        # 封装数据并发送API请求
        payload = {
            "prompt": f">>>><<<<中是用户对于某化妆品品牌的评论内容，请判断该评论内容是正面还是负面评价，如果是正面评价请回复正向评价，如果是负面评价请给出判断依据，如果是无法判断请告知无法判断。>>>>{data_to_process}<<<<",
            "max_tokens": 512,
            "temperature": 0.5,
            "num_beams": 4,
            "top_k": 40

        }
        # print(payload)# 修改成适合API的请求参数
        response = requests.post(api_url, json=payload, headers=headers)  # 发送POST请求，这里使用json格式发送数据

        # 处理API响应结果
        if response.status_code == 200:
            result_data = response.json()  # 假设API返回的数据是JSON格式
            choices = result_data.get('choices', [])
            if choices:
                text = choices[0].get('text', '')

                print(str(index+1)+". "+text)
                processed_result = text  # 假设API返回的结果在'result'字段中
            else:
                print("No 'choices' found in the response.")

        else:
            # processed_result = response.json()
            processed_result = 'API请求失败'  # 处理请求失败的情况

        # 在该行新增一列保存处理结果
        row['Processed_Result'] = processed_result

        # 将处理结果添加到列表中
        results.append(row)

    # 将处理结果列表转换为DataFrame
    result_df = pd.DataFrame(results)

    # 将结果保存到输出文件中
    result_df.to_excel(output_file, index=False)

def process_excel_files_in_directory(input_directory, output_directory, api_url, headers, column_name_to_process):
    # 确保输出目录存在
    os.makedirs(output_directory, exist_ok=True)

    # 列出目录中的所有Excel文件
    excel_files = [f for f in os.listdir(input_directory) if f.endswith('.xlsx')]

    # 处理每个Excel文件
    for excel_file in excel_files:
        input_file = os.path.join(input_directory, excel_file)
        output_file = os.path.join(output_directory, f'output_{excel_file}')
        process_excel_with_api(input_file, output_file, api_url, column_name_to_process, headers)
        print(f"{excel_file} 处理完成。")

# 示例用法
if __name__ == '__main__':
    input_directory = 'data'  # 输入目录，存放待处理的Excel文件
    output_directory = 'output'  # 输出目录，存放处理后的Excel文件
    api_url = 'http://43.130.26.100:19327/v1/completions'
    headers = {'Content-Type': 'application/json'}

    column_name_to_process = '内容'  # 需要处理的列的名称
    input_excel_file = 'LRL种草贴数据.xlsx'  # 输入Excel文件名
    output_excel_file = 'output/LRL种草贴数据.xlsx'  # 输出Excel文件名
    process_excel_with_api(input_excel_file, output_excel_file, api_url, column_name_to_process, headers)
    # process_excel_files_in_directory(input_directory, output_directory, api_url, headers, column_name_to_process)
