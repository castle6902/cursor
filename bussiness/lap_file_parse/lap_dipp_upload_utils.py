import os
import threading
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
import requests

import settings
from bussiness.dipp.dipp_file_utils import UploadServerError, UploadNetworkError, FileUploadError
from common.utils.df_chain_utils import PandasChain
from logger import log


def upload_template_file_to_dipp(url: str, template_save_path, token):
    try:

        log.info(f"开始推送文件到 {url}")
        # 获取文件名
        file_name = os.path.basename(template_save_path)

        # 读取文件内容
        with open(template_save_path, 'rb') as file:
            files = {
                'file': (file_name, file)
            }

            headers = {
                "Authorization": f"Bearer {token}",
                # "Content-Type": "multipart/form-data"

            }

            # 发送请求
            response = requests.post(
                # response = requests.put(
                url=url,
                files=files,
                # data=data,
                headers=headers,
                timeout=30000  # 设置超时时间
            )

        # # 获取响应的 elapsed 时间（请求耗时）
        # elapsed_time = response.elapsed

        # print(f"响应状态码: {response.status_code}, 接口耗时 {elapsed_time}")

        # if response.status_code in [200, 201]:
        #     # print("✅ 文件上传成功！")
        #     log.info(f"文件上传成功 {template_save_path}")
        #     try:
        #         result = response.json()
        #         log.info("服务器响应:", result)
        #     except:
        #         log.warning(f"服务器返回非JSON响应: {response.text}")
        # else:
        #     # 服务器返回错误状态码，抛出异常
        #     raise UploadServerError(response.status_code, response.text)
        log.info(
            f"\n=== 向 dipp 上传 excel ，请求响应 ===\n"
            f"URL: {response.request.url}\n"
            f"状态码: {response.status_code}\n"
            f"耗时: {response.elapsed.total_seconds():.2f}s\n"
            f"响应头: {dict(response.headers)}\n"
            f"响应体: {response.text[:500] + ('...' if len(response.text) > 500 else '')}"
        )
    except requests.exceptions.Timeout:
        error_msg = f"文件上传超时: {template_save_path}"
        log.error(error_msg)
        raise UploadNetworkError(error_msg)
    except requests.exceptions.ConnectionError:
        error_msg = f"网络连接错误: {template_save_path}"
        log.error(error_msg)
        raise UploadNetworkError(error_msg)
    except UploadServerError:
        # 已处理的服务器错误，直接向上传递
        raise
    except Exception as e:
        # 捕获其他未预料的异常，包装为业务异常
        error_msg = f"文件上传失败: {str(e)}"
        log.error(f"{error_msg}, 文件: {template_save_path}")
        raise FileUploadError(error_msg)


def upload_data_to_dipp(url: str, payload: list[dict[str, str]], token: str):
    log.info(f"开始进行上传数据准备到 {url}")
    # print(payload)

    headers = {
        "Authorization": f"Bearer {token}",
        # "Content-Type": "multipart/form-data"
    }

    try:
        response = requests.post(
            url=url,
            json={"entry": payload},  # 自动序列化为JSON并设置Content-Type
            # json=data,  # 自动序列化为JSON并设置Content-Type
            headers=headers,
            timeout=60,  # 超时时间（秒）
        )

        log.info(
            f"\n=== 向 dipp 上传数据，请求响应 ===\n"
            f"URL: {response.request.url}\n"
            f"状态码: {response.status_code}\n"
            f"耗时: {response.elapsed.total_seconds():.2f}s\n"
            f"响应头: {dict(response.headers)}\n"
            f"响应体: {response.text[:500] + ('...' if len(response.text) > 500 else '')}"
        )
    except ValueError:
        log.error("响应不是有效的JSON格式")
