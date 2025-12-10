import re

import pandas as pd

from bussiness.lap_file_parse.config_of_djz import DJZConfig
from bussiness.lap_file_parse.model import FileInfo
from common.utils.df_chain_utils import PandasChain
from common.utils.file_utils import detect_file_encoding


def replace_pattern(s):
    # 正则匹配 .数字. 结构，捕获中间的数字
    pattern = r'\.(\d+)\.'

    def replacer(match):
        num = int(match.group(1))
        # 仅处理1-26范围内的数字，超出则返回原始匹配内容
        if 1 <= num <= 26:
            letter = chr(ord('A') + num - 1)
            return letter
        else:
            # 大于26时返回原始的 .数字. 结构
            return match.group(0)

    res = re.sub(pattern, replacer, s)
    return res


def style_three_data_filter(df):
    # 日期统一改为 2025/01/07
    df["Clinical Chemistry"] = "2025/01/07"
    df['Sample name'] = df['Sample name'].apply(replace_pattern)
    return df


def djz_parse_style_three(file_info: FileInfo, header_of_template: list[str]):
    # def detect_file_encoding(file_path, sample_size=100):
    bianma = detect_file_encoding(file_path=file_info.save_path)
    # 读取 CSV 文件
    df = pd.read_csv(file_info.save_path, encoding=bianma, dtype=str)
    # df = df.fillna("").astype(str)  # 将 NaN 替换为空字符串后再转字符串
    # # 将所有值转换为字符串类型
    # # astype(str) 会将 NaN 转换为字符串 "nan"，如果需要处理空值可以在这里添加逻辑
    # df = df.astype(str)

    final_result_map = (PandasChain(df)
                        .read_as_str()
                        .header_trim()
                        # .header_rename_if_exist(djz_config.StyleThree.header_map_file_to_template)  # 名称转为 template 文件中的
                        .header_rename_if_exist(DJZConfig.header_map_file_to_template)  # 名称转为 template 文件中的
                        .column_select_need(header_of_template)  # 挑选 template 中有的列
                        .filter_column_with_function(style_three_data_filter)
                        .return_keyed_dict(keys=DJZConfig.file_join_columns)
                        )
    # print(f'======{file_info.save_path}================  three')
    # for key, value in final_result_map.items():
    #     print(f"{key}: {value}")
    return final_result_map
