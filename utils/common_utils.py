def dict_add(dict_obj, key_name, start_value=1, step=1):
    dict_obj[key_name] = dict_obj[key_name] + step if key_name in dict_obj.keys() else start_value