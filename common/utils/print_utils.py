def print_list(data: list):
    for index, item in enumerate(data):
        print(f"索引 {index}：{item}")  # 索引和元素分行显示


def print_dict(data: dict):
    for key, value in data.items():
        print(f"{key}: {value}")  # 键和值用冒号连接，分行显示
