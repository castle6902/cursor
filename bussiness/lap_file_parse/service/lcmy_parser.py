from typing import List

import pandas as pd

from bussiness.lap_file_parse.config_of_lcmy import LCMYConfig
from bussiness.lap_file_parse.model import FileInfo, LapFileType
from common.string_utils import special_flag_as_split
from common.utils.df_chain_utils import PandasChain
from common.utils.file_utils import detect_file_encoding
from logger import log


def get_new_header(first_row: list[str], second_row: list[str], header_map_digit: dict[str, str]):
    """ 将 header 全部转换为模板上的 header """
    res = []
    prefix_header = ""
    for index, header in enumerate(first_row):

        value_of_first_row = header.strip()
        value_of_second_row = second_row[index].strip()

        # ===========================================
        if len(value_of_first_row) == 0:
            change_prefix_header = False
            suffix_of_new_header = value_of_second_row
        else:
            # 第一行非空， 就不要变动了，直接使用第一行的header, 说明 prefix header变化了
            change_prefix_header = True
            prefix_header = value_of_first_row
            suffix_of_new_header = value_of_first_row

        # ===========================================
        if change_prefix_header:
            new_header = header_map_digit.get(prefix_header, prefix_header)
        else:
            # 没有出现变更 header, 就需要使用 prefix_header + suffix_of_new_header
            if len(prefix_header) == 0:
                # 说明是开头的几个，事没有 prefix 的。直接拿第二行替换即可
                new_header = header_map_digit.get(suffix_of_new_header, suffix_of_new_header)
            else:
                # 说明不是开头的几行，每一列都有自己的 prefix
                new_header = header_map_digit.get(prefix_header,
                                                  prefix_header) + special_flag_as_split + suffix_of_new_header

        res.append(new_header)

    return res


def select_alarm(csv_headers: list[str], template_header: list[str]) -> list[tuple[str, str]]:
    res = []  # 用于存储（基础列, 报警列）的配对结果
    for item in csv_headers:
        # 筛选以 "_Alm" 结尾的列（不区分大小写的话可改用 .lower().endswith("_alm")）
        if item.endswith("_Alm"):
            # 提取基础列名（分割 "_Alm" 前的部分）
            base_header = item.rsplit(special_flag_as_split, 1)[0]  # 比 split 更稳妥，避免基础列名含 "_"
            # 检查基础列是否在模板表头中
            if base_header in template_header:
                res.append((base_header, item))  # 将配对添加到结果列表
    return res


def conn_alarm(df, pair_alarm: list[tuple[str, str]]):
    log.info(f"需要匹配的列为 {pair_alarm}")

    def row_handler(row):
        res = []
        for base_col, alarm_col in pair_alarm:
            base_value = row[base_col]
            alarm_value = row[alarm_col]
            if len(alarm_value) == 0:
                continue
            else:
                info = f"{base_col}:{base_value}{alarm_value}"
                res.append(info)
                pass
        # 用逗号分隔所有部分
        return ", ".join(res)

    df["ERROR"] = df.apply(row_handler, axis=1)
    return df


def data_filter(df):
    # # 转换为 datetime 类型
    # df['date'] = pd.to_datetime(df['date'])
    #
    # # 格式化为 "YYYY/MM/DD"
    # df['date_formatted'] = df['date'].dt.strftime('%Y/%m/%d')

    # ===========================================================
    # 时间格式化
    # =========================================================
    df["Clinical Immunoassay"] = pd.to_datetime(df["Clinical Immunoassay"]).dt.strftime('%Y/%m/%d')  # 正确写法
    #
    # # uid 处理
    # df["Sample name"] = df["Sample name"].str.split("-").str[0]  # 正确写法

    # ===========================================================
    # 删除以 PC 开头的列
    # =========================================================
    # 筛选出 name 以 "test" 开头的行的索引
    # 注意：str.startswith() 区分大小写，若需忽略大小写可加参数 case=False
    df["Sample name"] = df["Sample name"].str.strip()  # 正确写法
    test_rows = df[df["Sample name"].str.startswith("PC", na=False)].index

    # 删除这些行（inplace=True 表示在原 DataFrame 上修改）
    df.drop(test_rows, inplace=True)
    return df


def one_file_parser(file_info: FileInfo, header_of_template: list[str]):
    # 告警所在的列

    # df = pd.read_csv(file_info.save_path, encoding='utf-8', header=None)
    bianma = detect_file_encoding(file_path=file_info.save_path)
    df = pd.read_csv(file_info.save_path, encoding=bianma, header=None)
    df = df.fillna("").astype(str)  # 将 NaN 替换为空字符串后再转字符串
    first_row = df.iloc[0].values.tolist()
    second_row = df.iloc[1].values.tolist()

    # 1、将第二行的值替换到第一行的空值上
    # 2、确认第一行的列掌控的数据范围
    # 3、将 header 替换为模板中的 header
    new_header = get_new_header(first_row=first_row, second_row=second_row,
                                header_map_digit=LCMYConfig.header_map_file_to_template)

    # 匹配出来 template 中的列， 和起对应的异常列
    # 获取到 [(INSULIN, INSULIN_xxx_alarm), (age, age_alarm)]
    template_header_with_alarm = select_alarm(csv_headers=new_header, template_header=header_of_template)

    # 2. 删除前两行（保留从第三行开始的数据）
    df = df[2:]  # 索引 0 和 1 是前两行，[2:] 表示从索引 2 开始取
    df.columns = new_header

    # 3、删除 pc 开头的列
    df = data_filter(df)

    df = conn_alarm(df, template_header_with_alarm)

    pd_chain = (PandasChain(df)
                .column_add_missing(header_of_template)
                .column_select_need(header_of_template)
                .row_remove_last_row()
                )  # 挑选 template 中才有的列

    return pd_chain


def lcmy_parser(lap_file_info_list: List[FileInfo], header_of_template: list[str]):
    log.info(f"开始解析【临床免疫】， 提取header{header_of_template}")
    # header_of_template.append("ERROR")
    base_chain = PandasChain.of_empty_with_headers(header_of_template)
    for file_info in lap_file_info_list:
        pandas_chain = one_file_parser(file_info=file_info, header_of_template=header_of_template)
        # base_chain.df_merge_missing_by_key(pandas_chain.df)
        base_chain.df_merge_vertically_append(other_df=pandas_chain.df)
    log.info(f"结束解析【临床免疫】， 提取完成")
    # 返回的结果是 （） 的样子
    return LapFileType.LCMY, base_chain
