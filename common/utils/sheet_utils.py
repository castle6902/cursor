def rename_empty_headers_with_index(headerStr: str, separator: str = ',', new_header_prefix: str = "COLUMN_"):
    """
    处理表头字符串，将空表头重命名为 COLUMN_数字（从1开始）

    参数:
        headerStr: 原始表头字符串（如 "ALT,TP,,GLU"）
        separator: 分隔符，默认为逗号 ','，可根据实际情况修改（如 '\t' 表示制表符）

    返回:
        处理后的表头列表
    """
    header_list = headerStr.split(separator)

    for i in range(len(header_list)):
        # 去除首尾空格后判断是否为空
        if not header_list[i].strip():
            header_list[i] = f"{new_header_prefix}{i}"

    return header_list


def rename_empty_headers_with_letter(headerStr: str, separator: str = ',', new_header_prefix: str = "COLUMN_"):
    """
    处理表头字符串，将空表头重命名为 COLUMN_数字（从1开始）

    参数:
        headerStr: 原始表头字符串（如 "ALT,TP,,GLU"）
        separator: 分隔符，默认为逗号 ','，可根据实际情况修改（如 '\t' 表示制表符）

    返回:
        处理后的表头列表
    """
    header_list = headerStr.split(separator)
    # 记录空表头的计数（从1开始，避免 COLUMN_0）

    for i in range(len(header_list)):
        # 去除首尾空格后判断是否为空
        if not header_list[i].strip():
            column_letter = number_to_excel_column_name(i)
            header_list[i] = f"{new_header_prefix}{column_letter}"

    return f'{separator}'.join(map(str, header_list))


def number_to_excel_column_name(index: int) -> str:
    """
    将数字索引转换为Excel风格的列名（0→A，1→B，...，25→Z，26→AA，27→AB...）

    参数:
        index: 从0开始的索引值

    返回:
        对应的Excel风格列名字符串
    """
    column_name = ""
    index += 1  # 转换为1-based索引，以便从A(1)开始对应

    while index > 0:
        # 计算当前位的偏移量（0-25对应A-Z）
        index -= 1
        # 获取当前位的字母（65是'A'的ASCII码）
        column_name = chr(index % 26 + 65) + column_name
        # 处理更高位
        index = index // 26

    return column_name


def rename_empty_headers_with_left(headerStr: str, separator: str = ',', new_header_prefix: str = "COLUMN_"):
    """
    A, , , ,B, ,C, D,
    A, A_1, A_2, A_3,B, B_1,C, D,

    参数:
        index: 从0开始的索引值

    返回:
        对应的Excel风格列名字符串
    """
    """
    处理表头字符串，将空表头重命名为 COLUMN_数字（从1开始）

    参数:
        headerStr: 原始表头字符串（如 "ALT,TP,,GLU"）
        separator: 分隔符，默认为逗号 ','，可根据实际情况修改（如 '\t' 表示制表符）

    返回:
        处理后的表头列表
    """
    header_list = headerStr.split(separator)
    # 记录空表头的计数（从1开始，避免 COLUMN_0）

    #
    start_header = "start"
    index = 1

    for i in range(len(header_list)):
        header = header_list[i].strip()
        if header:
            start_header = header
            index = 1
        else:
            header_list[i] = f"{start_header}_{index}"
            index = index + 1

    return f'{separator}'.join(map(str, header_list))
