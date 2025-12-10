class FileError(Exception):
    """文件操作异常基类"""

    def __init__(self, file_path: str, message: str = "文件操作失败"):
        self.file_path = file_path
        self.message = message
        super().__init__(f"{message} (文件: {file_path})")


# class FileNotFoundError(FileError):
#     """文件不存在异常"""
#
#     def __init__(self, file_path: str):
#         super().__init__(file_path, "文件不存在或路径错误")
class FileDownLoadError(FileError):
    """文件类型异常,无法解析该类异常"""

    def __init__(self, file_path: str, message: str = "文件下载异常"):
        super().__init__(file_path, message=message)


class FileParsedError(FileError):
    """文件类型异常,无法解析该类异常"""

    def __init__(self, file_path: str, message: str = "文件解析异常"):
        super().__init__(file_path, message=message)


class FileUploadError(FileError):
    """文件类型异常,无法解析该类异常"""

    def __init__(self, file_path: str, message: str = "文件上传异常"):
        super().__init__(file_path, message=message)


class FileTypeError(FileError):
    """文件类型异常,无法解析该类异常"""

    def __init__(self, file_path: str, message: str):
        super().__init__(file_path, message=message)


class FilePermissionError(FileError):
    """文件权限异常"""

    def __init__(self, file_path: str, mode: str):
        super().__init__(file_path, f"无权限以 '{mode}' 模式访问文件")


class FileFormatError(FileError):
    """文件格式异常"""

    def __init__(self, file_path: str, expected_format: str):
        super().__init__(file_path, f"文件格式不符合要求，应为 {expected_format}")


class FileSizeExceededError(FileError):
    """文件大小超限异常"""

    def __init__(self, file_path: str, max_size_mb: int):
        super().__init__(file_path, f"文件大小超过限制（最大允许 {max_size_mb}MB）")


class FileLockedError(FileError):
    """文件被锁定异常"""

    def __init__(self, file_path: str, process_name: str = None):
        msg = "文件被其他进程占用" + (f"（进程: {process_name}）" if process_name else "")
        super().__init__(file_path, msg)
