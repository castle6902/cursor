import pandas as pd

from bussiness.lap_file_parse.config_of_djz import DJZConfig
from bussiness.lap_file_parse.model import FileInfo
from common.utils.df_chain_utils import PandasChain
from common.utils.file_utils import detect_file_encoding


def data_filter(df):
    # 日期统一改为 2025/01/07
    df["Clinical Chemistry"] = "2025/01/07"
    # 你的原代码就是正确的
    df['HbA1c'] = df['HbA1c'].str.replace('%', '')
    return df


def djz_parse_style_hba1c(file_info: FileInfo, header_of_template: list[str]):
    # csv_file_path = "./source/HbA1c原始数据1.xlsx"
    # csv_file_path = "./source/HbA1c原始数据2.xlsx"

    # 1、将第二行的值替换到第一行的空值上
    # 2、确认第一行的列掌控的数据范围
    # 3、将 header 替换为模板中的 header
    # new_header = get_new_header(first_row=first_row, second_row=second_row, header_map_digit=header_map_digit)

    # 从 template 中解析出来的 header

    # 读取Excel（假设数据从 A1 开始，没有标题行）
    # df = pd.read_excel(file_save_path, sheet_name=XcgConfig.data_sheet, header=None)
    # df = pd.read_excel(file_info.save, sheet_name=0, header=1, dtype=str)

    # def detect_file_encoding(file_path, sample_size=100):
    bianma = detect_file_encoding(file_path=file_info.save_path)
    df = pd.read_csv(file_info.save_path, encoding=bianma, dtype=str, header=1)

    file_data_map = (PandasChain(df)
                     .read_as_str()
                     .header_rename_if_exist(DJZConfig.header_map_file_to_template)  # 表头重命名为 template 中的
                     .column_select_need(header_of_template)  # 选择 template 需要的
                     # 这个的顺序貌似有问题，如果获取的字段不存在就会爆异常，需要做try catch 处理
                     .filter_column_with_function(data_filter)
                     # "Clinical Chemistry": "date",
                     # "Sample name": "samplename",
                     .return_keyed_dict(keys=DJZConfig.file_join_columns)
                     # 以
                     )

    # print(f'======{file_info.save_path}================ hba1c')
    # for key,value in file_data_map.items():
    #     print(f"{key}: {value}")

    return file_data_map
