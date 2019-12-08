def dict_add(dict_obj, key_name, start_value=1, step=1):
    dict_obj[key_name] = dict_obj[key_name] + step if key_name in dict_obj.keys() else start_value


def sort_by_dict(items: list, args: dict, key: str):
    """
    根据列表中的顺序重新排序列表字典 冒泡排序法
    :param items: 待排序列表字典
    :param args: 参考字典 key为排序对象 value为优先级
    :param key: 参考字段
    :return: None
    """
    length = len(items)
    for i in range(length):
        for j in range(1, length):
            if args[items[j-1][key]] > args[items[j][key]]:
                items[j-1], items[j] = items[j], items[j-1]