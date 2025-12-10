"""
血常规里面，主要是 excel 文件， 针对 excel 文件进行解析
"""
import os
from concurrent.futures import wait
from datetime import datetime
from typing import List

import pandas as pd

from bussiness.lap_file_parse.config_of_xcg import XCGConfig

from bussiness.lap_file_parse.model import LapFileTransfer, FileInfo, LapFileType

from common.utils.df_chain_utils import PandasChain

from logger import log


def file_data_filter(df):
    # 格式化时间
    df["Hematology"] = pd.to_datetime(df["Hematology"]).dt.strftime('%Y/%m/%d')  # 正确写法
    # 删除空的行
    df = df[df["Sample name"] != '']
    return df


def one_file_parser(file_info: FileInfo, header_of_template: list[str]):
    try:
        # 文件下载，下载到本地
        # def download_file(file_download_url, token, file_save_path) -> str:
        log.debug(f"开始解析文件 {file_info.save_path} ")

        # 读取Excel（假设数据从 A1 开始，没有标题行）
        # df = pd.read_excel(file_save_path, sheet_name=XcgConfig.data_sheet, header=None)
        df = pd.read_excel(file_info.save_path, sheet_name=0, header=None, dtype=str)

        chain_df = (PandasChain(df)
                    .read_as_str()
                    .transpose_select_first_column_as_header()
                    .header_rename_if_exist(XCGConfig.header_map_file_to_template)  # 表头重命名为 template 中的
                    .column_add_missing(header_of_template)
                    .column_select_need(header_of_template)
                    # 这个的顺序貌似有问题，如果获取的字段不存在就会爆异常，需要做try catch 处理
                    .filter_column_with_function(file_data_filter)
                    )
        return chain_df
    except KeyError as e:
        log.error(f"错误: 列名 '{e}' 不存在，请检查模板映射或数据格式。")
    except Exception as e:
        log.error(f"文件 {file_info.save_path} 解析遇到异常 {e}")

    # 存在异常就会犯空的对象


def xcg_parser(lap_file_info_list: List[FileInfo], header_of_template: list[str]):
    """
    方案一： 直接写入 csv
    :param header_of_template:
    :param lap_file_info_list:
    :return:
    """
    log.info(f"开始解析【血常规】， 提取header{header_of_template}")
    base_chain = PandasChain.of_empty_with_headers(header_of_template)
    for file_info in lap_file_info_list:
        pandas_chain = one_file_parser(file_info=file_info, header_of_template=header_of_template)
        # base_chain.df_merge_missing_by_key(pandas_chain.df)

        base_chain.df_merge_vertically_append(other_df=pandas_chain.df)

    log.info(f"结束解析【血常规】， 提取完成")
    return LapFileType.XCG, base_chain
