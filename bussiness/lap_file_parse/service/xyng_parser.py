from typing import List
import chardet
import pandas as pd

from bussiness.lap_file_parse.config_of_xyng import XYNGConfig
from bussiness.lap_file_parse.model import FileInfo, LapFileType
from common.utils.df_chain_utils import PandasChain
from common.utils.file_utils import detect_file_encoding
from logger import log


def data_filter(df):
    # # 转换为 datetime 类型
    # df['date'] = pd.to_datetime(df['date'])
    #
    # # 格式化为 "YYYY/MM/DD"
    # df['date_formatted'] = df['date'].dt.strftime('%Y/%m/%d')

    # df["Hematology"] = pd.to_datetime(df["Hematology"])  # 正确写法
    # 直接用 .loc 定位列，先转为 datetime 再格式化，避免警告
    df.loc[:, "Blood Coagulation"] = pd.to_datetime(
        df["Blood Coagulation"],
        format="%Y.%m.%d",  # 匹配原始格式：年.月.日（支持单数月/日，如1.4）
        errors="coerce"  # 无法解析的日期会转为 NaT
    ).dt.strftime("%Y/%m/%d")  # 转为 年/月/日 格式（单数会保留，如1/4）
    return df


def one_file_parser(file_info: FileInfo, header_of_template: list[str]):
    csv_file_path = file_info.save_path
    bianma = detect_file_encoding(file_path=file_info.save_path)

    df = pd.read_csv(csv_file_path, encoding=bianma)
    df = df.fillna("").astype(str)  # 将 NaN 替换为空字符串后再转字符串

    pd_chain = (PandasChain(df)
                .header_rename_if_exist(XYNGConfig.header_map_file_to_template)
                .column_add_missing(header_of_template)
                .column_select_need(header_of_template)
                .filter_column_with_function(data_filter)
                )  # 挑选 template 中才有的列

    return pd_chain


def xyng_parser(lap_file_info_list: List[FileInfo], header_of_template: list[str]):
    """
    方案一： 直接写入 csv
    :param header_of_template:
    :param lap_file_info_list:
    :return:
    """
    log.info(f"开始解析【血液凝固】， 提取header{header_of_template}")
    base_chain = PandasChain.of_empty_with_headers(header_of_template)
    for file_info in lap_file_info_list:
        pandas_chain = one_file_parser(file_info=file_info, header_of_template=header_of_template)
        # base_chain.df_merge_missing_by_key(pandas_chain.df)

        base_chain.df_merge_vertically_append(other_df=pandas_chain.df)
    log.info(f"结束解析【血液凝固】， 提取完成")
    # base_chain.print()
    return LapFileType.XYNG, base_chain
