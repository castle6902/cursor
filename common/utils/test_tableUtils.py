from common.utils.sheet_utils import rename_empty_headers_with_index, rename_empty_headers_with_letter, \
    number_to_excel_column_name


def test_rename_empty_headers_with_index():
    # 测试用例1：逗号分隔，包含空表头
    test_header1 = "ALT,TP,,GLU,,T-CHO"
    print(rename_empty_headers_with_index(test_header1))
    # 输出: ['ALT', 'TP', 'COLUMN_1', 'GLU', 'COLUMN_2', 'T-CHO']

    # 测试用例2：制表符分隔（模拟Excel导出的TSV文件）
    test_header2 = "AST\tALP\t\tTBIL"
    print(rename_empty_headers_with_index(test_header2, separator='\t'))
    # 输出: ['AST', 'ALP', 'COLUMN_1', 'TBIL']


def test_rename_empty_headers_with_letter():
    # 测试用例1：逗号分隔，包含空表头
    test_header1 = "ALT,TP,,GLU,,T-CHO"
    print(rename_empty_headers_with_letter(test_header1))
    # 输出: ['ALT', 'TP', 'COLUMN_1', 'GLU', 'COLUMN_2', 'T-CHO']

    # 测试用例2：制表符分隔（模拟Excel导出的TSV文件）
    test_header2 = "AST\tALP\t\tTBIL"
    print(rename_empty_headers_with_letter(test_header2, separator='\t'))
    # 输出: ['AST', 'ALP', 'COLUMN_1', 'TBIL']


def test_number_to_excel_column_name():

    print(number_to_excel_column_name(15))
    print(number_to_excel_column_name(27))
    print(number_to_excel_column_name(30))

