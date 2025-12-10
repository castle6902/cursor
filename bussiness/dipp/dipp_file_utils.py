import uuid
import os
import re
import requests
from urllib.parse import unquote, urlparse

from bussiness.dipp.model import DippFileTransfer
from logger import log


# 定义业务异常类，使调用方可以更精准地捕获
class FileUploadError(Exception):
    """文件上传相关异常的基类"""
    pass


class FileNotFoundError(FileUploadError):
    """文件不存在异常"""
    pass


class UploadNetworkError(FileUploadError):
    """网络相关错误"""
    pass


class UploadServerError(FileUploadError):
    """服务器返回错误状态码"""

    def __init__(self, status_code: int, response_text: str):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"服务器返回错误状态码: {status_code}, 详情: {response_text}")


def get_filename_from_response(response):
    # 1. 从 Content-Disposition 提取
    if "Content-Disposition" in response.headers:
        cd = response.headers["Content-Disposition"]
        print(cd)
        match = re.search(r'filename="?([^";]+)"?', cd)
        if match:
            return unquote(match.group(1))

    # 2. 从 URL 路径提取
    path = urlparse(response.url).path
    return unquote(os.path.basename(path))


def download_file(file_download_url, token, file_save_path):
    """

    :param file_download_url:  文件下载的路径
    :param token:  文件下载的时候使用的 token
    :param file_save_path:  文件下载下来后保存的 abstractPath
    :return:
    """

    headers = {"Authorization": f"Bearer {token}"}
    log.info(f"开始从 dipp 中下载文件 {file_download_url} 到 文件 {file_save_path}")
    # 文件下载
    response = requests.get(file_download_url,
                            headers=headers,
                            allow_redirects=True,
                            stream=True,  # 流式下载
                            timeout=600)

    if response.status_code not in range(200, 300):
        # 非成功状态，抛出异常或记录错误
        response.raise_for_status()  # 自动抛出 HTTPError 异常（推荐）
        # 或手动处理：
        # log.error(f"请求失败，状态码: {response.status_code}，响应内容: {response.text[:100]}")
        # return False  # 终止后续流程

    # 文件保存到本地
    with open(file_save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    log.info(f"文件下载完成: {file_save_path}")


def download_and_rename_with_ext(url, new_name, headers, save_dir=None):
    response = requests.get(url, headers=headers, allow_redirects=True)

    original_name = get_filename_from_response(response)

    # 保留原扩展名
    base, ext = os.path.splitext(original_name)
    final_name = f"{new_name}{ext}" if ext else new_name

    # 如果未指定 save_dir，则保存到当前目录
    if save_dir is None:
        save_dir = os.path.join(os.getcwd(), "ZWFile", "bkExcel")

    # 如果目录不存在，则创建
    os.makedirs(save_dir, exist_ok=True)
    # 拼接完整路径
    file_path = os.path.join(save_dir, final_name)
    absolute_path = os.path.abspath(file_path)

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return absolute_path


def upload_file_to_dipp(abstract_file_path, request: DippFileTransfer):
    """ 文件上传 """
    # 检查文件是否存在
    if not os.path.exists(abstract_file_path):
        error_msg = f"文件 {abstract_file_path} 不存在"
        log.error(error_msg)
        raise FileNotFoundError(error_msg)

    # 检查文件扩展名

    # 构建完整的 URL（替换 fieldName）

    try:
        # 获取文件名
        file_name = os.path.basename(abstract_file_path)

        # 读取文件内容
        with open(abstract_file_path, 'rb') as file:
            files = {
                'file': (file_name, file)
            }

            headers = {
                "Authorization": f"Bearer {request.token}",
                # "Content-Type": "multipart/form-data"

            }

            url = request.upload_file_url()

            # 发送请求
            response = requests.post(
                # response = requests.put(
                url=url,
                files=files,
                # data=data,
                headers=headers,
                timeout=30  # 设置超时时间
            )

        # 获取响应的 elapsed 时间（请求耗时）
        elapsed_time = response.elapsed

        # print(f"响应状态码: {response.status_code}, 接口耗时 {elapsed_time}")

        if response.status_code in [200, 201]:
            # print("✅ 文件上传成功！")
            log.info(f"文件上传成功 {abstract_file_path}")
            try:
                result = response.json()
                log.info("服务器响应:", result)
            except:
                log.warning(f"服务器返回非JSON响应: {response.text}")
        else:
            # 服务器返回错误状态码，抛出异常
            raise UploadServerError(response.status_code, response.text)

    except requests.exceptions.Timeout:
        error_msg = f"文件上传超时: {abstract_file_path}"
        log.error(error_msg)
        raise UploadNetworkError(error_msg) from None
    except requests.exceptions.ConnectionError:
        error_msg = f"网络连接错误: {abstract_file_path}"
        log.error(error_msg)
        raise UploadNetworkError(error_msg) from None
    except UploadServerError:
        # 已处理的服务器错误，直接向上传递
        raise
    except Exception as e:
        # 捕获其他未预料的异常，包装为业务异常
        error_msg = f"文件上传失败: {str(e)}"
        log.error(f"{error_msg}, 文件: {abstract_file_path}")
        raise FileUploadError(error_msg) from e
