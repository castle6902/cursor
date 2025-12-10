from bussiness.lap_file_parse.model import LapFileType, FileInfo
from common.excel_utils import excel_read_xlsx, excel_read_xlsx_with_multi_sheet

from logger import log


# def template_file_of_xlsx_parse(file_path:str, sheet_name:str) -> list[str]:
#     """ 解析 template 文件 """
#     # 将 excel 拆分合并单元格后读取为 pandas
#     pf = excel_read_xlsx(file=file_path, sheet_name=sheet_name)
#
#     # 返回第二行，作为 header
#     return PandasChain(pf).return_row_data_type_use_list(row_index=1)

def template_file_of_xlsx_parse(file_info: FileInfo, sheet_name_list: list[LapFileType]) -> dict[
    LapFileType, list[str]]:
    """ 解析 template 文件，返回每个指定 sheet 的第二行数据（作为 header） """
    # 存储每个 sheet 的第二行数据（key: sheet 名称, value: 第二行数据列表）
    log.info(f"获取 sheet 中的header: {sheet_name_list}")
    res = {}

    # 将枚举列表转换为对应的 sheet 名称字符串（如 LapFileType.XCG → "XCG"）
    sheet_names = [sheet_type.value for sheet_type in sheet_name_list]

    # 读取 Excel 中指定的 sheet（返回字典：{sheet_name: DataFrame}）
    # 注意：file_info 的 save_path 是字符串路径，直接传入即可

    pf_map = excel_read_xlsx_with_multi_sheet(file=file_info.save_path, sheet_names=sheet_names)

    # 遍历每个指定的 sheet，提取第二行数据（索引为 1，因为 pandas 从 0 开始计数）
    for sheet_type in sheet_name_list:
        sheet_name = sheet_type.value  # 获取枚举对应的字符串名称

        if sheet_name in pf_map:  # 确保 sheet 存在于读取结果中
            # iloc[1] 取第二行数据，转换为列表
            second_row = pf_map[sheet_name].iloc[1].values.tolist()
            second_row.append("ERROR")
            # 删除空白
            cleaned_row = [s.strip() for s in second_row]
            
            # ====================================================
            # 处理化学电解质 sheet 中的 CO2 这个化合物
            # 将 CO₂ 或 CO2（带下标）统一改为 CO2
            # ====================================================
            if sheet_type == LapFileType.SHDJZ:
                # 使用正则表达式匹配 CO2 的各种变体（包括下标）
                import re
                # 匹配 CO 后面跟数字（可能是下标）的模式，统一替换为 CO2
                cleaned_row = [re.sub(r'CO[₂2]?', 'CO2', header, flags=re.IGNORECASE) for header in cleaned_row]
            
            res[sheet_type] = cleaned_row

    # 根据需求，若需返回所有 sheet 的第二行合并列表，可使用：
    # return [row for rows in res.values() for row in rows]
    # 若需返回按 sheet 名称映射的字典，直接返回 res（需修改函数返回类型注解为 dict）

    return res
