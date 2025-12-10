def filter_dicts_by_keys(list_of_dicts, target_keys):
    """
    data = [
        {"name": "Alice", "age": 25, "city": "New York", "job": "Engineer"},
        {"name": "Bob", "age": 30, "country": "USA"},
        {"name": "Charlie", "city": "London", "language": "English"}
    ]
    
    # 我们只关心的键
    keys_to_keep = ["name", "age", "city"]
    
    方法结果（只保留存在的键）:
    [{'name': 'Alice', 'age': 25, 'city': 'New York'}, 
     {'name': 'Bob', 'age': 30}, 
     {'name': 'Charlie', 'city': 'London'}]
    """

    filtered_list = []
    for d in list_of_dicts:
        # 只保留目标键，如果键不存在则不包含该键或设为None
        # filtered_dict = {key: d.get(key) for key in target_keys}
        filtered_dict = {key: d[key] for key in target_keys if key in d}
        filtered_list.append(filtered_dict)
    return filtered_list


def filter_dicts_by_keys_with_none(list_of_dicts, target_keys):
    """
    data = [
        {"name": "Alice", "age": 25, "city": "New York", "job": "Engineer"},
        {"name": "Bob", "age": 30, "country": "USA"},
        {"name": "Charlie", "city": "London", "language": "English"}
    ]

    # 我们只关心的键
    keys_to_keep = ["name", "age", "city"]

    方法结果（只保留存在的键）:
    [{'name': 'Alice', 'age': 25, 'city': 'New York'}, 
     {'name': 'Bob', 'age': 30}, 
     {'name': 'Charlie', 'city': 'London'}]
    """

    filtered_list = []
    for d in list_of_dicts:
        # 只保留目标键，如果键不存在则不包含该键或设为None
        filtered_dict = {key: d.get(key) for key in target_keys}
        filtered_list.append(filtered_dict)
    return filtered_list


def filter_dicts_by_key_map_new_key(data, key_mapping):
    """
    data = [
        {"name": "Alice", "age": 25, "city": "New York", "job": "Engineer"},
        {"name": "Bob", "age": 30, "country": "USA"},
        {"name": "Charlie", "city": "London", "language": "English"}
    ]

    # 我们只关心的键
    target_keys_map = {
        "name": "name",
        "age":  "bigAge",
        "city": "cidy"
    }

    方法结果（只保留存在的键）:
    [{'name': 'Alice', 'bigAge': 25, 'city': 'New York'},
     {'name': 'Bob', 'bigAge': 30},
     {'name': 'Charlie', 'city': 'London'}]
    """
    transformed_data = []
    for item in data:
        # 创建一个新字典，只包含key_mapping中存在的键，并进行重命名
        transformed_item = {}
        for original_key, new_key in key_mapping.items():
            if original_key in item:
                transformed_item[new_key] = item[original_key]
        transformed_data.append(transformed_item)
    return transformed_data


def list_dict_flatten(combine_list_dict):
    """
    [
        {name: zhangsan},
        {age: 40},
        {gender: nana}
    ]

    ||

    {
        name: zhangsan,
        age: 40,
        gender: nana,
    }

    后来的 key 会覆盖前面的key



    :param data:
    :return:
    """
    combined_map = {}

    # 遍历 results 列表中的每个字典
    for item in combine_list_dict:
        # 跳过可能为 None 的异常结果
        if item is not None:
            # 将每个小字典的键值对合并到总字典中
            combined_map.update(item)
    return combined_map









