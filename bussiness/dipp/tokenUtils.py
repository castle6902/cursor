import requests
import json
from requests import Timeout

from bussiness.dipp.exception import TokenFetchError


def fetchTokenOfTest():
    url = "https://dipptest.wuxiapptec.com/magicflu/jwt"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }  # 请求头
    data = {
        "j_username": "system",
        "j_password": "system"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        # 检查响应状态码
        # 检查响应状态码
        response.raise_for_status()

        # 解析响应内容
        # response_data = response.json()

        return response.json().get("token")
    except Timeout as e:
        raise TokenFetchError(f"请求超时: {e}") from e
    except requests.exceptions.RequestException as e:
        raise TokenFetchError(f"请求发生错误: {e}")
    except json.JSONDecodeError:
        raise TokenFetchError(f"响应内容不是有效的JSON格式")
    except Exception as e:
        raise TokenFetchError(f"处理响应时发生未知错误: {e}")


def fetchTokenOfPro():
    return ""


# if __name__ == '__main__':
#     token = fetchTokenOfTest()
#     print(token)
