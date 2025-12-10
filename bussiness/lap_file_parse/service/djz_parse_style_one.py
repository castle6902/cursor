import json

import pandas as pd

from io import StringIO

from bussiness.lap_file_parse.config_of_djz import DJZConfig
from bussiness.lap_file_parse.model import FileInfo

from common.utils.df_chain_utils import PandasChain
from common.utils.file_utils import detect_file_encoding

from common.utils.sheet_utils import rename_empty_headers_with_letter
from logger import log


# def merge_son_table(final_result_map, son_data_map):
#     """
#     相同 key 的行进行合并
#     :param final_result_map:
#     :param df:
#     :return:
#     """
#     for key, data_map in son_data_map.items():
#         # 生成键：time-code
#
#         # 　获取　ｋｅｙ　对应
#         row_map = final_result_map.setdefault(key, {})
#         err_info = strings_join(row_map.setdefault('ERROR', ''), row_map.setdefault('ERROR', ''))
#
#         row_map = row_map | value
#
#         row_map['ERROR'] = err_info
#
#         final_result_map[key] = row_map


def style_one_data_filter(df):
    # # 转换为 datetime 类型
    # df['date'] = pd.to_datetime(df['date'])
    #
    # # 格式化为 "YYYY/MM/DD"
    # df['date_formatted'] = df['date'].dt.strftime('%Y/%m/%d')

    # df["Hematology"] = pd.to_datetime(df["Hematology"])  # 正确写法
    # 日期统一改为 2025/01/07
    df["Clinical Chemistry"] = "2025/01/07"

    # uid 处理
    df["Sample name"] = df["Sample name"].replace(r"-011$", "", regex=True)  # 正确写法

    # ===========================================================
    # 确认异常列的左侧是哪一列
    # =========================================================
    # 更改 header,
    current_headers = list(df.columns)
    # #
    error_column_to_header_map = {}
    # # # 查找到需要删除的列，这些列应该是序号列
    start_header = current_headers[0]
    # start_index = 1
    for index, header in enumerate(current_headers[1:], 1):
        if header.startswith("COLUMN_"):
            # rename_header_map[header] = f"{start_header}_{start_index}"
            # start_index = start_index + 1
            error_column_to_header_map[header] = start_header
            pass
        else:
            # 说明碰到了非 COLUMN_ 开头的列
            start_header = header

    # ===========================================================
    # 拼接异常列
    # =========================================================
    def row_handler(row):
        parts = []

        # 遍历每一行
        for error_info_column, header in error_column_to_header_map.items():

            # error_info_column : HEADER  COLUMN_A
            # column : HEADER
            # error_flag : >
            # row[column] : HEADER 列对应的值

            # 异常的标志，  比如  >    =  row[ COLUMN_A ]
            error_flag = row[error_info_column]

            if not pd.isna(error_flag) and error_flag != '':
                # 格式："{tag} {row[col]} {tag}"
                # 1000 > CO2
                # value 1000 不会有空格，  flag 不会有空格， header 是指定的，不会有空格
                # part = f"{row[header]}:{error_flag}:{header}"
                part = f"{header}:{row[header]}:{error_flag}"
                # part = f"{column}_{row[column]} {error_flag} {column}"

                parts.append(part)
        # 用逗号分隔所有部分
        return ",".join(parts)

    df["ERROR"] = df.apply(row_handler, axis=1)
    return df


def djz_parse_style_one(file_info: FileInfo, header_of_template: list[str]):
    log.debug("开始解析样式1")


    # def detect_file_encoding(file_path, sample_size=100):
    bianma = detect_file_encoding(file_path=file_info.save_path)

    with open(file_info.save_path, 'r', encoding=bianma) as f:
        lines = f.readlines()
    header_lines_index = []
    cleaned_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith(','):
            pass
        else:
            # if "日期" in line and "轮次号" in line and "ID" in line:
            # if line.startswith("日期"):
            if "日期" in line and "SID" in line:
                header_lines_index.append(len(cleaned_lines))
            cleaned_lines.append(line)
    header_lines_index.append(len(cleaned_lines))

    # 获取 子table 的上下索引
    """
    [10, 20, 30, 40, 50]
    (10, 20)  # 第1个元素和第2个元素配对
    (20, 30)  # 第2个元素和第3个元素配对
    (30, 40)  # 第3个元素和第4个元素配对
    (40, 50)  # 第4个元素和第5个元素配对
    """
    pairs = list(zip(header_lines_index[:-1], header_lines_index[1:]))

    # =============================================
    # 解析子表
    # =============================================
    final_result_map = {}
    for i, pair in enumerate(pairs):
        # print(cleaned_lines[pair[0]:pair[1]])
        # tableData 是每个小表的数据，加上表头
        tableData = cleaned_lines[pair[0]:pair[1]]
        headers = rename_empty_headers_with_letter(tableData[0])
        # 遍历 header
        # 注意空列header被命名为了
        # for i, header in enumerate(headers):

        # print(header)
        tableData[0] = headers
        # # 将列表转为 CSV 字符串，用 pd.read_csv 解析
        # # df = pd.read_csv(StringIO("\n".join(tableData)), usecols=selected_columns)
        df = pd.read_csv(StringIO("\n".join(tableData)))
        #
        # ===========================================================

        # 删除位置列，就是
        delete_site_header = []
        current_headers = list(df.columns)
        for index, header in enumerate(current_headers[1:], 1):

            if not header.startswith("COLUMN_"):

                pre_header = current_headers[index - 1]
                if pre_header.startswith("COLUMN_"):
                    delete_site_header.append(pre_header)
        df.drop(columns=delete_site_header, errors='ignore', inplace=True)
        #
        # ===========================================================
        # 将所有 "*" 替换为 NaN（空值），
        df.replace("*", pd.NA, inplace=True)  # 直接修改 df
        # 清空空值列，这里清除掉
        df.dropna(axis=1, how="all", inplace=True)  # 原 df 被修改

        #
        data_map = (PandasChain(df)
                    # .header_trim()   # 标题栏
                    .read_as_str()  # 处理为 str
                    # .header_rename_if_exist(djz_config.StyleOne.header_map_file_to_template)  # 名称改为 template 的
                    .header_rename_if_exist(DJZConfig.header_map_file_to_template)  # 名称改为 template 的
                    .filter_column_with_function(style_one_data_filter)
                    .column_select_need(header_of_template)  # 挑选需要的 header
                    .return_keyed_dict(keys=DJZConfig.file_join_columns)
                    )  # 挑选 template 中才有的列

        # merge_son_table(final_result_map, df=df)
        final_result_map = DJZConfig.merge_file_key_map(final_result_map, data_map)

    # print(f'======{file_info.save_path}================  one')
    # for key, value in final_result_map.items():
    #     print(f"{key}: {value}")
    return final_result_map
