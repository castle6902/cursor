from typing import Dict, Tuple, Any, List

from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill

from bussiness.lap_file_parse.config_of_djz import DJZConfig
from bussiness.lap_file_parse.service.djz_parse_style_hba1c import djz_parse_style_hba1c
from bussiness.lap_file_parse.service.djz_parse_style_one import djz_parse_style_one
from bussiness.lap_file_parse.service.djz_parse_style_three import djz_parse_style_three
from bussiness.lap_file_parse.service.djz_parse_style_two import djz_parse_style_two
from bussiness.lap_file_parse.model import LapFileTransfer, FileInfo, LapFileType

from common.exception.file_exception import FileDownLoadError

from common.utils.df_chain_utils import PandasChain
from logger import log
import chardet


def one_file_parser(file_info: FileInfo, header_of_template: list[str]) -> dict[str, dict[str, str]]:
    file_save_path = file_info.save_path

    with open(file_save_path, 'rb') as f:
        # 读取样本数据（避免读取整个大文件）
        raw_data = f.read(1024)
    result = chardet.detect(raw_data)
    file_info.bianma = result['encoding']
    # bianma = result['encoding']

    # 根据第一行判断到底是哪个文件
    # with open(file_save_path, 'r', encoding=bianma) as f:
    with open(file_save_path, 'r', encoding=file_info.bianma) as f:
        first_line = f.readline()  # 读取第一行，返回字符串（包含换行符\n）

    # if first_line.startswith("日期,轮次号,ID,SID,批号,"):
    if "日期" in first_line and "SID" in first_line:
        log.debug("样式文件 1 的解析")
        # djz_parse_style_one(file_info: FileInfo, header_of_template: list[str], bianma: str):
        file_data_map = djz_parse_style_one(file_info=file_info, header_of_template=header_of_template)
        pf_type = "master"
    # elif first_line.startswith("样本序号,样本条码,样本类型,检测项目"):
    elif "完成时间" in first_line and "患者姓名" in first_line:
        log.debug("样式文件 2 的解析")

        file_data_map = djz_parse_style_two(file_info=file_info, header_of_template=header_of_template)
        pf_type = "master"
    # elif first_line.startswith("ID, Date , Time , Serial , PID ,"):
    elif "Date" in first_line and "PID" in first_line:
        log.debug("样式文件 3 的解析")
        file_data_map = djz_parse_style_three(file_info=file_info, header_of_template=header_of_template)
        pf_type = "slave"
    elif first_line.startswith("This file is tab-delimited"):
        # elif "Test Cartridge Scan Date/Time" in first_line and "Sample ID" in first_line:
        # "Sample ID": "Sample name",
        # "Test Cartridge Scan Date/Time": "Clinical Chemistry",
        log.debug("糖化血红蛋白")
        file_data_map = djz_parse_style_hba1c(file_info=file_info, header_of_template=header_of_template)
        pf_type = "slave"
    else:
        #  def __init__(self, file_path: str, message: str = "文件下载异常"):
        raise FileDownLoadError(file_path=file_save_path,
                                message=f"下载到的文件第一行，无法识别是哪种类型的文件，{first_line}")

    log.info(f"文件解析结束")
    return file_data_map


def djz_parser(lap_file_info_list: List[FileInfo], header_of_template: list[str]):
    log.info(f"开始解析【化学电解质-生化】， 提取header{header_of_template}")

    # header_of_template.append("ERROR")

    final_result = {}
    # index = 1
    for file_info in lap_file_info_list:
        file_data_map = one_file_parser(file_info=file_info, header_of_template=header_of_template)

        final_result = DJZConfig.merge_file_key_map(small_file_data=file_data_map, big_file_data=final_result)

        # print(f"==================================================")
        # for key, value in file_data_map.items():
        #     print(f" ===  {key} {value}")
        # print(f"--------------------------------------------------")
        # for key, value in final_result.items():
        #     print(f" ---  {key} {value}")
        # print(f"==================================================")
    log.info(f"结束解析【化学电解质-生化】， 提取完成, 开始写入 excel 中")
    pd_chain = (PandasChain
                .of_dict(list(final_result.values()))
                .column_add_missing(header_of_template)
                .column_select_need(header_of_template))

    return LapFileType.SHDJZ, pd_chain
