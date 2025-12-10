# 用来作为分隔符的，生僻度极高，无实际业务含义，适合对符号外观无要求的场景。
special_flag_as_split = "⦀"

def strings_join(*args, separator: str = ",") -> str:
    """
    拼接多个字符串参数，用指定分隔符分隔，忽略空字符串和纯空白字符串

    :param args: 任意数量的字符串参数
    :param separator: 分隔符（默认是逗号 ","）
    :return: 拼接后的字符串（无有效参数时返回空字符串）
    """
    # 过滤空字符串和纯空白字符串（仅保留有效字符串）
    non_empty_strings = [
        s for s in args
        if isinstance(s, str) and s.strip() != ""  # 确保是字符串且非空/非空白
    ]
    # 用指定分隔符拼接
    return separator.join(non_empty_strings)




def test_strings_join():
    # 1. 默认分隔符（逗号）
    print(strings_join("苹果", "", "香蕉", "  ", "橙子"))  # 输出：苹果,香蕉,橙子

    # 2. 自定义分隔符（分号）
    print(strings_join("张三", "李四", "", "王五", separator=";"))  # 输出：张三;李四;王五

    # 3. 自定义分隔符（竖线）
    print(strings_join("a", "b", "  ", "c", separator="|"))  # 输出：a|b|c

    # 4. 全是空值（返回空字符串）
    print(strings_join("", None, 123, separator="-"))  # 输出：""
