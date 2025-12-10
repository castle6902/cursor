from typing import Any

import pandas as pd
from pandas import DataFrame

from common.excel_utils import excel_read_xlsx
from logger import log
from common.utils.list_utils import list_select_repeat


class PandasChain:

    def __init__(self, df: DataFrame):  # 正确构造函数
        self.df = df

    @staticmethod
    def of_key_as_header(data: list[dict[Any, Any]]):
        return PandasChain(df=pd.DataFrame(data))

    @staticmethod
    # def of_dict(data: list[dict[Any, Any]]):
    def of_dict(data: list[dict[Any, Any]]):
        return PandasChain(df=pd.DataFrame(data, dtype=str))

    @staticmethod
    def of_empty_with_headers(headers: list[str]):
        return PandasChain(df=pd.DataFrame(columns=headers))

    def read_as_str(self, fillStr: str = ""):
        self.df = self.df.fillna(fillStr).astype(str)
        return self

    def transpose_select_first_column_as_header(self):
        """
        df 转置，然后第一列作为 header
        :return:
        """
        # # 转置 DataFrame（行变列，列变行）
        # transposed = df.transpose()
        # header = transposed.iloc[0].tolist()
        # data = transposed.iloc[1:]  # 从第1行（第二行）开始到最后
        # new_df_method1 = pd.DataFrame(data.values, columns=header)

        # 转置 DataFrame（行变列，列变行）
        transposed = self.df.transpose()

        # 设置第一行作为列名（ID, name, age, source）
        transposed.columns = transposed.iloc[0]
        # 第 0 行是行索引
        # 第一行是header
        transposed = transposed[1:]  # 去掉原第一行
        self.df = transposed
        return self

    def column_select_need(self, select_headers: list[str]):
        """
        按照 select_headers 的顺序挑选需要的列，没有的忽略
        :return:
        """
        # template_headers = list(template_header_map.keys())
        # print(template_headers)
        csv_headers = self.df.columns
        canBeSelectedHeaders = list_select_repeat(select_headers, csv_headers)
        self.df = self.df[canBeSelectedHeaders]
        return self

    def header_trim(self):
        """
        删除  header 左右的特殊字符
        :return:
        """
        header_list = self.df.columns.tolist()
        self.df.columns = [s.strip() for s in header_list]
        return self

    def filter_column_with_function(self, function):
        self.df = function(self.df)
        return self

    def header_rename_if_exist(self, rename_heads_map: dict[str, str]):
        """
        存在的 header 才会重命名, 注意【顺序不会变】
        :param rename_heads_map:
        :return:
        """
        header_list = self.df.columns.tolist()
        need_rename_headers = list(rename_heads_map.keys())
        for header in need_rename_headers:

            if header in header_list:
                index = header_list.index(header)
                header_list[index] = rename_heads_map[header]
        self.df.columns = header_list

        return self

    def column_add_columns(self, header_list: list[str], default_value: str = ""):
        """
        提那家一个
        :param header_list:
        :param default_value:
        :return:
        """
        for header in header_list:
            self.df[header] = default_value
        return self

    def column_add_column(self, header: str, default_value: str = ""):
        """
        给 pandas 添加一个列，该列的值全部填充为 default_value
        :param header:
        :param default_value:
        :return:
        """
        self.df[header] = default_value
        return self

    def column_add_missing(self, source_header: list[str], default_value: str = ""):
        """
        对于 source_header 中的 header, 如果不存在与 self.df 则添加上该列，并将该列全部填充为  default_value
        :param source_header:
        :param default_value:
        :return:
        """
        header_list = self.df.columns.tolist()
        for header in source_header:
            if header not in header_list:
                self.df[header] = default_value

        return self

    def row_remove_with_unequal(self, header, value):
        self.df = self.df[self.df[header] != value]
        return self

    def row_remove_with_equal(self, header, value):
        self.df = self.df[self.df[header] != value]
        return self

    def row_remove_empty_nan(self):
        """
        删除所有的空行，对于替换换掉的 ”“ 需要使用 replace 将 "" 替换为 nan
        :return:
        """
        self.df = self.df.dropna(how='all')
        return self

    def row_remove_last_row(self):
        # 获取最后一行的索引（默认索引下为 df.index[-1]）
        last_row_index = self.df.index[-1]

        # 删除最后一行
        self.df = self.df.drop(last_row_index)
        return self

    """
    # 1. 左联（left join）：保留左表所有行，匹配右表数据
left_join = pd.merge(
    df_left,
    df_right,
    how='left',  # 左联
    on='id'      # 连接列
)

# 2. 右联（right join）：保留右表所有行，匹配左表数据
right_join = pd.merge(
    df_left,
    df_right,
    how='right',  # 右联
    on='id'
)

# 3. 全连接（outer join）：保留左右表所有行
outer_join = pd.merge(
    df_left,
    df_right,
    how='outer',  # 全连接
    on='id'
    
    merge 用法
        1、指定对比的列，就是 on, 相同的就和并，不同的就直接插入
        2、对于非指定的列：非 on, 的，就是重命名一个列名，双方都保持
        
        
===================================================================

    update 只会更新左侧有的列
    # 2. 用right_df覆盖left_df中ID匹配的行（只覆盖ID=2、3）
    left_df.update(right_df)

    
    
)
    
    """

    # def df_left_join(self, df, columns: list[str]):
    #     self.df = pd.merge(
    #         self.df,
    #         df,
    #         how='left',  # 左联
    #         on=columns  # 连接列
    #     )
    #     return self
    #
    # def df_right_join(self, df, columns: list[str]):
    #     self.df = pd.merge(
    #         self.df,
    #         df,
    #         how='right',  # 左联
    #         on=columns  # 连接列
    #     )
    #     return self
    #
    # def df_outer_join(self, df: DataFrame, columns: list[str]):
    #
    #     self.df = pd.merge(
    #         self.df,
    #         df,
    #         how='outer',  # 左联
    #         on=columns  # 连接列
    #     )
    #     return self
    #
    # def df_bottom_join(self, df: DataFrame, dfs: list[DataFrame] = None):
    #     if dfs is None:
    #         self.df = pd.concat([self.df, df], ignore_index=True)
    #         return self
    #     else:
    #         dfs = [self.df] + dfs
    #         self.df = pd.concat(dfs, ignore_index=True)
    #         return self

    # def df_merge_missing_by_key(self, source_df: DataFrame, primary_header: list[str]):

    # =================================================
    # 注意：所有的 merge 都必须要保持列名一致，都需要提前保持列名一致
    # =================================================

    def df_merge_missing_by_key(self, source_df: DataFrame, primary_header: list[str]):
        """
        函数的逻辑是：
            1、以 primary_header 为索引，将 self.df 和 source_df 进行对齐
            2、对于索引（即 primary_header 组合）在 self.df 中已存在的行：
                a、保留 self.df 中原有的非缺失值 【就是说原本的值不会被覆盖，】
                b、用 source_df 中的值填充 self.df 中缺失的部分（如果 source_df 对应位置有值的话）
            3、对于索引在 self.df 中不存在但在 source_df 中存在的行：
                从 source_df 完整添加到 self.df 中
        简单说就是：以自身数据为基础，用源数据补充缺失值并新增自身没有的行。如果 self.df 中某行的某个字段已有值，即使 source_df 中对应字段有不同值，也不会被覆盖（这一点和 “用新的值更新到当前值中” 的表述略有差异，需要注意


        :param source_df: 就是当前的额 df 需要更新 + 添加右侧  source_df 中的值
        :param primary_header:  通过 update_header 确认为同一行
        :return:
        """

        self.df = self.df.set_index(primary_header)
        source_df = source_df.set_index(primary_header)

        self.df = self.df.combine_first(source_df).reset_index()
        return self

    """
    result = pd.merge(
    df_left,
    df_right,
    how='outer',
    left_on=['id_left', 'class_left'],  # 左表连接列
    right_on=['id_right', 'class_right']  # 右表连接列
)
    """

    def df_merge_vertically_append(self, other_df: DataFrame = None, other_dfs: list[DataFrame] = None):
        """
        1. 轴方向的指定
        上下拼接本质是沿 0 轴（行轴） 进行合并（axis=0，这是 pd.concat() 的默认值）。
        想象两个表格 “摞起来”：第一个表格的最后一行后面直接接上第二个表格的第一行。
        2. 列的对齐规则
        拼接时会根据列名自动对齐列，具体规则：
        列名相同的部分：对应列的值会纵向拼接（同一列下的数据依次排列）。
        列名不同的部分：不存在该列的 DataFrame 会用 NaN 填充缺失值
        :return:
        """
        if other_df is not None:
            self.df = pd.concat([self.df, other_df], axis=0, ignore_index=True)
        elif other_dfs is not None:
            # 组合当前 df 和列表中的所有 df，形成待拼接的列表
            dfs_to_concat = [self.df] + other_dfs
            # 执行纵向拼接
            self.df = pd.concat(dfs_to_concat, axis=0, ignore_index=True)
        return self

    def return_dict(self):
        return self.df.to_dict("records")

    def return_dict_without(self, delete_value: str = ""):
        original_dict = self.df.to_dict("records")
        # 过滤条件：值不是 None，且不是空字符串，且不是空列表
        # filtered_dict = {
        #     k: v
        #     for k, v in enumerate(original_dict)
        #     if v is not None or v != value
        # }

        return [
            {key: value for key, value in d.items() if value is not None and value != delete_value and not pd.isna(value)}
            for d in original_dict
        ]

    def return_keyed_dict(self, keys: list[str], seperator: str = ":"):
        """
        某一行的值为  【k1:1，k1:2，k1:3】 组成以 k1, k2 为键值对的 dict{1:2: {k1:1，k1:2，k1:3}}
        :param seperator:
        :param keys:
        :param key:
        :return:
        """
        return {
            # 取每行中keys对应的value，转为字符串后用separator拼接作为key
            seperator.join(map(str, row[keys])): row.to_dict()
            for _, row in self.df.iterrows()
        }

    def return_df(self):
        return self.df

    def return_header_list(self):
        """
        获取当前的 pandas 的 所有列明
        :return:
        """
        return self.df.columns

    def return_row_data_type_use_list(self, row_index: int):
        """ 将第几行的数据以数组的形式返回 """
        return self.df.iloc[row_index].values.tolist()

    def order_by(self, headers):
        """
        单列排序	df.sort_values(by="列名")
        多列联合排序	df.sort_values(by=["列1", "列2"])
        不同列不同排序方式	df.sort_values(by=["列1", "列2"], ascending=[True, False])
        处理缺失值	df.sort_values(by="列名", na_position="first")
        原地排序	df.sort_values(by="列名", inplace=True)
        :return:
        """
        self.df = self.df.sort_values(headers)
        return self

    def write_to_excel(self, file_path):
        """  Excel 写入时是按列顺序匹配的，而不是按列名匹配  """
        pass

    def print_dict(self):
        data = self.return_dict()
        print()
        for datum in data:
            print(datum)

    def print(self):
        print(self.df.to_string(max_cols=None))  # max_cols=None 显示所有列
