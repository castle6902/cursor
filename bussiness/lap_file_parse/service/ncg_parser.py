from typing import List

import pandas as pd

from bussiness.lap_file_parse.config_of_ncg import NCGConfig
from bussiness.lap_file_parse.model import FileInfo, LapFileType
from common.utils.df_chain_utils import PandasChain
from logger import log


def data_filter(df):
    # # 转换为 datetime 类型
    # df['date'] = pd.to_datetime(df['date'])
    #
    # # 格式化为 "YYYY/MM/DD"
    # df['date_formatted'] = df['date'].dt.strftime('%Y/%m/%d')

    # df["Hematology"] = pd.to_datetime(df["Hematology"])  # 正确写法
    # 日期统一改为 2025/01/07
    df["Urinalysis"] = "2025/01/07"
    test_rows = df[df["Sample name"].str.startswith("UC-CONTROL", na=False)].index

    # 删除这些行（inplace=True 表示在原 DataFrame 上修改）
    df.drop(test_rows, inplace=True)
    return df


def one_file_parser(file_info: FileInfo, header_of_template: list[str]):

    df = pd.read_excel(file_info.save_path, sheet_name=0, dtype=str)

    chain_df = (PandasChain(df)
                .read_as_str()
                # .header_trim()
                .header_rename_if_exist(NCGConfig.header_map_file_to_template)  # 表头重命名为 template 中的
                .column_add_missing(header_of_template)
                .column_select_need(header_of_template)
                # 这个的顺序貌似有问题，如果获取的字段不存在就会爆异常，需要做try catch 处理
                .filter_column_with_function(data_filter)
                )
    # chain_df.print()
    # log.info(f" === {header_of_template} ")

    return chain_df


def ncg_parser(lap_file_info_list: List[FileInfo], header_of_template: list[str]):
    log.info(f"开始解析【尿常规】， 提取header{header_of_template}")
    base_chain = PandasChain.of_empty_with_headers(header_of_template)
    for file_info in lap_file_info_list:
        pandas_chain = one_file_parser(file_info=file_info, header_of_template=header_of_template)
        # base_chain.df_merge_missing_by_key(pandas_chain.df)
        base_chain.df_merge_vertically_append(other_df=pandas_chain.df)
    log.info(f"结束解析【尿常规】， 提取完成")
    return LapFileType.NCG, base_chain
