from filetype import filetype
from logger import log


class FileTypeParsedError(Exception):
    def __init__(self, message):
        super().__init__(f"获取到超出预期之外的文件类型 {message}")


def get_file_type(file_path):
    """用filetype库判断文件类型（轻量版）"""
    kind = filetype.guess(file_path)
    if not kind:
        log.error("遇到无法解析的文件的魔数，文件为 {file_path}")
        raise FileTypeParsedError(f"遇到无法解析的文件的魔数")

    return kind.extension
