from common.utils.list_dict_utils import filter_dicts_by_keys, filter_dicts_by_key_map_new_key


def test_filter_dicts_by_keys():
    # 示例数据：包含额外字段的字典列表
    data = [
        {'name': 'Alice', 'age': 30, 'gender': 'Female', 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'gender': 'Male', 'occupation': 'Engineer'},
        {'name': 'Charlie', 'age': 35, 'city': 'London'}  # 缺少gender字段
    ]

    # 目标键列表
    target_keys = ['name', 'age', 'gender']

    # 筛选处理
    result = filter_dicts_by_keys(data, target_keys)

    # 输出结果
    for item in result:
        print(item)


def test_transform_dicts():
    # 示例数据
    data = [
        {"name": "Alice", "age": 25, "city": "New York", "job": "Engineer"},
        {"name": "Bob", "age": 30, "country": "USA"},
        {"name": "Charlie", "city": "London", "language": "English"}
    ]

    # 键名映射
    target_keys_map = {
        "name": "name",
        "age": "bigAge",
        "city": "cidy"  # 注意：这里有个拼写错误，应该是 "city" 还是故意写成 "cidy"？
    }

    # 转换数据
    transformed_data = filter_dicts_by_key_map_new_key(data, target_keys_map)

    # 打印结果
    print(transformed_data)

