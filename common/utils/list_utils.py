from itertools import chain
def list_intersection(list1, list2):
    """
    计算两个数组的交集
    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) & set(list2))


def list_select_repeat(list1, list2):
    """
    按照 list1 的顺序，选择出 list1 和 list2 的交集
    :param list1:
    :param list2:
    :return:
    """
    res = []
    for e in list1:
        if e in list2:
            res.append(e)

    return res


def list_merge(list1, list2):
    """
    合并两个数组：
    a = [1, 2, 3]   +  b = [4, 5, 6]  ==》 [1, 2, 3, 4, 5, 6]
    :param list1:
    :param list2:
    :return:
    """
    return list(chain(list1, list2))


def list_join_delete_empty_to_str(data: list[str]):
    pass






