"""
这个专门用于发送http请求
"""
from typing import Any

import requests
import json


def send_post_request(host_url: str, token, payload: list[Any]):
    """

    :param host_url:
    :param token:
    :param data:
    :return:
    """

    # 1. 设置请求头（根据接口要求配置）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        # 注意：发送JSON数据时，requests会自动添加Content-Type: application/json
        # 如需发送其他类型数据，需手动指定，如表单数据使用application/x-www-form-urlencoded
    }

    # 2. 准备请求数据（根据接口要求选择合适的格式）
    # 2.1 JSON格式数据（最常用）
    try:
        # 3. 发送POST请求（根据数据类型选择合适的参数）
        # 3.1 发送JSON数据（推荐使用json参数）
        response = requests.post(
            url=host_url,
            json=payload,  # 自动序列化为JSON并设置Content-Type
            headers=headers,
            timeout=10  # 超时时间（秒）
        )

        # 4. 检查请求状态（200-299表示成功）
        response.raise_for_status()

        # 5. 处理响应结果
        print(f"请求成功！状态码: {response.status_code}")
        print("响应头信息:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")

        print("\n响应内容:")
        # 尝试解析JSON响应
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            # 非JSON响应，直接打印文本
            print(response.text)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")  # 4xx客户端错误或5xx服务器错误
    except requests.exceptions.ConnectionError:
        print("连接错误: 无法连接到服务器，请检查URL或网络")
    except requests.exceptions.Timeout:
        print("超时错误: 请求超过指定时间未响应")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
    finally:
        # 如果有文件上传，确保关闭文件
        # if 'file_payload' in locals():
        #     for file in file_payload.values():
        #         file.close()
        pass
