import os
from datetime import datetime
from pathlib import Path
from typing import Any

import settings
from logger import log


class DJZConfig:
    # 同一批请求的excel下载的时候，会有一个同意的前缀
    template_sheet_name = "Clinical Chemistry"

    file_join_columns = ['Clinical Chemistry', 'Sample name']

    header_map_template_to_dipp = {
        "Clinical Chemistry": "date",
        "Sample name": "samplename",
        "ALT": "alt",
        "TP": "tp",
        "GLU": "glu",
        "T-CHO": "tcho",
        "ALB": "alb",
        "AST": "ast",
        "ALP": "alp",
        "TBIL": "tbil",
        "UREA": "urea",
        "CREA": "crea",
        "UA": "ua",
        "TG": "tg",
        "CK": "ck",
        "P": "p",
        "CA": "ca",
        "GGT": "ggt",
        "HDL-C": "hdlc",
        "LDL-C": "ldlc",
        "RF": "rf",
        "CRP": "crp",
        "LDH": "ldh",
        "DBIL": "dbil",
        "GLB": "glb",
        "A/G": "ag",
        "CO2": "co2",
        "AST/ALT": "astalt",
        "ApoC3": "apoc3",
        "Lp.a": "lpa",
        "I-Bil": "ibil",
        "NEFA": "nefa",
        "D3H": "d3h",
        "IgM": "igm",
        "IgA": "iga",
        "IgG": "igg",
        "IgE": "ige",
        "GLDH": "gldh",
        "TBA": "tba",
        "Apo B": "apob",
        "C3": "c3",
        "C4": "c4",
        "CYS-C": "cysc",
        "Mg": "mg",
        "Apo E": "apoe",
        "cTnI": "ctni",
        "ACE": "ace",
        "Fer": "fer",
        "Fe": "fe",
        "UIBC": "uibc",
        "TIBC": "tibc",
        "TSAT": "tsat",
        "NonHDL-c": "nonhdlc",
        "hs-CRP": "hscrp",
        "LPS": "lps",
        "TPUC": "tpuc",
        "mALB": "malb",
        "K": "k",
        "Na": "na",
        "Cl": "cl",
        "HbA1c": "hba1c",
        "ERROR": "error"
    }
    header_map_file_to_template = {
        # ----------------------------------
        # 样式一
        # ----------------------------------
        "日期": "Clinical Chemistry",
        "SID": "Sample name",
        # ----------------------------------
        # 样式二
        # ----------------------------------
        '患者姓名': 'Sample name',
        '完成时间': 'Clinical Chemistry',
        # ----------------------------------
        # 样式三
        # ----------------------------------
        "PID": "Sample name",
        "Date": "Clinical Chemistry",
        # ----------------------------------
        # 糖化血红蛋白
        # ----------------------------------
        "Sample ID": "Sample name",
        "Test Cartridge Scan Date/Time": "Clinical Chemistry",
        "%HbA1c Result": "HbA1c",
        # ----------------------------------
        # 通用的
        # ----------------------------------
        "CHOL": "T-CHO",
        "Ca": "CA",
        "Apo C3": "ApoC3",
        "APOC3": "ApoC3",
        "LPa": "Lp(a)",
        "D3-H": "D3H",
        "ApoB": "Apo B",
        "APOB": "Apo B",
        "ApoE": "Apo E",
        "IRON": "Fe",
        "Non-HDL-C": "NonHDL-c",
        "CL": "Cl",
        "GLO": "GLB",
        "IBIL": "I-Bil",

    }

    @staticmethod
    def merge_file_key_map(small_file_data: dict[str, dict[str, str]], big_file_data: dict[str, dict[str, str]]):
        """
        合并两个嵌套字典：以small_file_data为基准，将键值对合并到big_file_data中
        相同key的值用逗号拼接（小字典值在前，大字典值在后），优化性能（小字典遍历）
        :param small_file_data: 小字典（被合并的基准）
        :param big_file_data: 大字典（合并后的结果存储）
        :return: 合并后的big_file_data
        """

        def flat_list_dict(small_row_map: dict[str, str], big_row_map: dict[str, str]):
            # 遍历小字典的键，合并到大字典
            for key, small_value in small_row_map.items():
                small_value = small_value.strip()
                big_value = big_row_map.get(key, "").strip()  # 获取大字典当前键的值
                # 收集非空值，按“小字典值在前”拼接
                if small_value == big_value:
                    merged_value = small_value
                else:
                    merged_value = f"{small_value},{big_value}"
                merged_value = merged_value.strip(',')
                if len(merged_value) != 0:
                    big_row_map[key] = merged_value

            return big_row_map

        # 遍历小字典的顶层键，合并到大字典
        for top_key, small_row in small_file_data.items():
            # 初始化大字典中不存在的顶层键为{}（避免类型错误）
            big_row = big_file_data.get(top_key, {})
            # 合并当前顶层键下的键值对
            big_file_data[top_key] = flat_list_dict(small_row, big_row)
        return big_file_data


class StyleOne(DJZConfig):
    header_map_file_to_template = DJZConfig.header_map_file_to_template


class StyleTwo:
    header_map_file_to_template = {
        '患者姓名': 'Sample name',
        '完成时间': 'Clinical Chemistry',
        'CL': 'Cl'
    }


class StyleThree:
    header_map_file_to_template = {
        "PID": "Sample name",
        "Date": "Clinical Chemistry",
    }
