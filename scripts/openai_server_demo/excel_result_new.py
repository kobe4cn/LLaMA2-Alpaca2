import time
import pandas as pd
import requests
import os
def process_excel_with_api(input_file, output_file, api_url, column_to_process, headers):
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
        request_count=0
        # while True:
            # 封装数据并发送API请求
        payload = {
            "prompt": f'请判断>>>><<<<中的评论是正面还是负面评价。>>>>{data_to_process}<<<<',
            "max_tokens": 512,
            "temperature": 0.7,
            "num_beams": 3,
            "top_k": 50
        }

        # 发送POST请求，这里使用json格式发送数据
        response = requests.post(api_url, json=payload, headers=headers)

        # 处理API响应结果
        if response.status_code == 200:
            result_data = response.json()  # 假设API返回的数据是JSON格式
            choices = result_data.get('choices', [])
            if choices:
                text = choices[0].get('text', '')

                print(str(index + 1) + ". " + text)
                processed_result = text  # 假设API返回的结果在'result'字段中

                # # 判断是否需要重新请求
                # if "无法判断" in processed_result or "负面" in processed_result:
                #     print("Re-requesting API...")
                #     time.sleep(2)  # 等待2秒再次请求
                # else:
                #     break  # 得到正面评价的结果，退出循环
            else:
                print("No 'choices' found in the response.")
                break  # 没有choices字段，退出循环
        else:
            processed_result = 'API请求失败'  # 处理请求失败的情况
            break

            # if request_count >= 2:
            #     break
            # request_count+=1
        # 在该行新增一列保存处理结果
        row['Processed_Result'] = processed_result

        # 将处理结果添加到列表中
        results.append(row)

        # 每500条记录追加写入一次输出的Excel文件
        if len(results) == 500:
            result_df = pd.DataFrame(results)
            # result_df.to_excel(output_file, index=False, mode='a', header=False)
            with pd.ExcelWriter(output_file, mode='a', engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False, header=False)
            results = []  # 清空列表


    # 将剩余的处理结果追加写入输出的Excel文件
    if results:
        result_df = pd.DataFrame(results)
        # result_df.to_excel(output_file, index=False, mode='a', header=False)
        with pd.ExcelWriter(output_file, mode='a', engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False, header=False)
# 示例用法
if __name__ == '__main__':
    input_excel_file = 'LRL种草贴数据.xlsx'  # 输入Excel文件名
    output_excel_file = 'output/LRL种草贴数据.xlsx'  # 输出Excel文件名
    api_url = 'http://43.130.26.100:19327/v1/completions'
    headers = {'Content-Type': 'application/json'}

    column_name_to_process = '内容'  # 需要处理的列的名称

    process_excel_with_api(input_excel_file, output_excel_file, api_url, column_name_to_process, headers)
