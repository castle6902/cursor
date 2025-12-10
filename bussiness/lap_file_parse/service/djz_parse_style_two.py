import pandas as pd

from bussiness.lap_file_parse.config_of_djz import DJZConfig
from bussiness.lap_file_parse.model import FileInfo
from common.string_utils import special_flag_as_split
from common.utils.df_chain_utils import PandasChain


def style_two_data_filter(df):
    # 日期统一改为 2025/01/07
    df["完成时间"] = "2025/01/07"
    return df


def style_two_after_rename_filter(df):
    """在header重命名后处理SID后缀删除"""
    if "Sample name" in df.columns:
        df["Sample name"] = df["Sample name"].replace(r"-011$", "", regex=True)
    return df


def djz_parse_style_two(file_info: FileInfo, header_of_template: list[str]):

    # 读取 CSV 文件
    df = pd.read_csv(file_info.save_path, encoding=file_info.bianma, dtype=str)
    # df = df.fillna("").astype(str)  # 将 NaN 替换为空字符串后再转字符串
    # 将所有值转换为字符串类型
    # astype(str) 会将 NaN 转换为字符串 "nan"，如果需要处理空值可以在这里添加逻辑
    # df = df.astype(str)
    #
    json_data = (PandasChain(df).read_as_str()
                 .header_trim()
                 .column_select_need(["完成时间", "患者姓名", "检测项目", "检测值"])
                 .filter_column_with_function(style_two_data_filter)
                 .order_by(["完成时间", "患者姓名"])
                 .return_dict()
                 )

    records_result = {}
    for json_datum in json_data:
        riqi = json_datum["完成时间"]
        sid = json_datum["患者姓名"]
        key = json_datum["检测项目"].strip()
        value = json_datum["检测值"]
        records_key = f"{riqi}{special_flag_as_split}{sid}"
        if records_key in records_result:
            records_result[records_key][key] = value
        else:
            records_result[records_key] = {"完成时间": riqi, "患者姓名": sid, f"{key}": value}

    final_result_map = (PandasChain
                        # .of_key_as_header(list_dict_flatten(records_result.values()))   # 构建 df
                        .of_dict(list(records_result.values()))  # 构建 df
                        .header_trim()
                        .read_as_str()
                        # .header_rename_if_exist(djz_config.StyleTwo.header_map_file_to_template)  # 重命名为 template 中的列
                        .header_rename_if_exist(DJZConfig.header_map_file_to_template)  # 重命名为 template 中的列
                        .column_select_need(header_of_template)  # 选择 template 中仅有的列
                        .filter_column_with_function(style_two_after_rename_filter)  # SID 需要去除掉 -011 后缀
                        .return_keyed_dict(keys=DJZConfig.file_join_columns)
                        )
    # print(f'======{file_info.save_path}================  two')
    # for key, value in final_result_map.items():
    #     print(f"{key}: {value}")
    return final_result_map
