# 1. 定义自定义异常（继承自Exception）
class FileTypeError(Exception):
    """自定义异常：文件类型不符合要求"""

    def __init__(self, file_type, expected_types):
        self.file_type = file_type
        self.expected_types = expected_types
        # 调用父类构造函数，设置异常信息
        super().__init__(f"不支持的文件类型: {file_type}，期望类型: {expected_types}")


# class FileSizeError(Exception):
#     """自定义异常：文件大小超出限制"""
#
#     def __init__(self, size, max_size):
#         super().__init__(f"文件大小超出限制: {size}MB，最大支持: {max_size}MB")


class TokenFetchError(Exception):
    def __init__(self, message):
        super().__init__(f"token 获取解析异常 {message}")
