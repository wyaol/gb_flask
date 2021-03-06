import os
import re
import datetime
import xlrd
from utils.common_utils import dict_add, sort_by_dict


def _get_filename_by_partname(chooses, partname):
    for choose in chooses:
        if partname in choose: return choose
    return None


def _get_file_path_by_keyword(path, keyword):
    files = os.listdir(path)
    choose = _get_filename_by_partname(files, keyword)
    if choose is None: raise FileNotFoundError()
    return '%s%s' % (path, choose)


def __get_width(length):
    """
    根据该列的相对最多字节数计算该列的前端需要的长度
    :param length: 该列最多的字节数
    :return int: 该列的宽度 前端单位为px
    """
    res = 0
    if length < 4:
        res = length * 20 + 20
    elif 4 <= length < 8:
        res = 100 + (length - 4) * 10
    else:
        res = 140 + (length - 8) * 7.5
    return res


def __get_table_head_line(table, row_num, col_num):
    """
    获取表格表头行数 以备注列所占的空间为标准
    :param table: 表格对象
    :param row_num: 行数
    :param col_num: 列数
    :return:
    """
    count = 1
    for i in range(row_num):
        for j in range(col_num):
            if table.cell(i, j).value == '备注':
                for k in range(i + 1, row_num):
                    if table.cell(k, j).value == '':
                        count += 1
                    else:
                        return count
                return count
    return None


def _get_table_struct(path, head_line=None):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    row_num = table.nrows
    col_num = table.ncols

    res = []
    history = []

    # 计算每列的长度
    col_word_count_max = [0] * col_num
    for i in range(col_num):
        for j in range(row_num):
            value = table.cell(j, i).value
            if type(value) is str and len(value) > 0 and value[0] == '注': continue
            count = len(str(value)) // 2 if type(value) is float else len(value)
            col_word_count_max[i] = col_word_count_max[i] if count < col_word_count_max[i] else count

    if head_line is None:
        head_line = __get_table_head_line(table, row_num, col_num)
    if head_line is None: head_line = row_num

    for i in range(head_line):
        row = []
        for j in range(col_num):
            value = table.cell(i, j).value
            if value == '':
                continue

            item = {'title': value, 'width': __get_width(col_word_count_max[j])}

            # 便利以自身为左上角起点的矩形区域占几个单元格
            for ii in range(i + 1, row_num):
                if table.cell(ii, j).value == '' and (ii, j) not in history:
                    history.append((ii, j))
                    dict_add(item, 'rowspan', 2)
                else:
                    break
            for jj in range(j + 1, col_num):
                if table.cell(i, jj).value == '' and (i, jj) not in history:
                    history.append((i, jj))
                    dict_add(item, 'colspan', 2)
                else:
                    break

            if ('rowspan' in item and (i + item['rowspan'] - 1 == head_line - 1)) or i == head_line - 1:
                item['field'] = str(j)
            item['align'] = 'center'  # 表格居中
            row.append(item)
        res.append(row)
    return res


def _get_table_data(path, head_line):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    row_num = table.nrows
    col_num = table.ncols
    res = []
    if head_line is None:
        head_line = __get_table_head_line(table, row_num, col_num)
    if head_line is None: head_line = 0
    for i in range(head_line, row_num):
        row = []
        for j in range(col_num):
            value = table.cell(i, j).value
            cell_type = table.cell(i, j).ctype
            if cell_type == 3:
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(value, data.datemode)
                py_date = datetime.datetime(year, month, day)
                value = py_date.strftime("%Y-%m-%d")
            row.append(value)
        res.append(row)
    return res


def _get_table_cont(path, line=None):
    res_array = _get_table_data(path, line)
    res = []
    for cols in res_array:
        row = {}
        for i in range(len(cols)):
            value = cols[i]
            row[str(i)] = value if type(value) is not float else round(value, 3)
        res.append(row)
    return res


def get_size_weight_table_head(path):
    return _get_table_struct(_get_file_path_by_keyword(path, '尺寸'))


def get_size_weight_table_cont(path, limit, page):
    res = _get_table_cont(_get_file_path_by_keyword(path, '尺寸'))
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur: (cur + limit)]
    return res, count


def get_tree():
    return _get_tree('中机数据', [])


def _get_tree(dir, dirs):
    try:
        res = []
        p_dirs = os.listdir(dir)
        for dir_n in p_dirs:
            new_dirs = dirs.copy()
            new_dirs.append(dir_n)
            new_dir = os.path.join(dir, dir_n)
            dirss = os.listdir(new_dir)
            if len(dirss) != 0:
                new_dir_dir = os.path.join(new_dir, dirss[0])
                os.listdir(new_dir_dir)
            ress = {
                'name': dir_n,
                'id': new_dirs
            }
            result = _get_tree(new_dir, new_dirs)
            if result is not None:
                ress['children'] = result
            res.append(ress)
        return res
    except NotADirectoryError:
        return None


def get_tree2():
    # fasteners = []
    res = {}
    p_dirs = os.listdir('中机数据/')
    for dir_n in p_dirs:
        dirs = os.listdir('中机数据/%s/' % dir_n)
        res[dir_n] = []
        for i in range(len(dirs)):
            res[dir_n].append({'id': '%s/%s' % (dir_n, dirs[i]), 'name': dirs[i]})

    sort_by_dict(res['紧固件'], {
        '螺栓': 0,
        '螺柱': 1,
        '螺母': 2,
        '螺钉': 3,
        '木螺钉': 4,
        '自攻螺钉': 5,
        '垫圈': 6,
        '销': 7,
        '铆钉': 8,
        '挡圈': 9,
        '组合件和连接副': 10,
        '焊钉': 11,
    }, 'name')

    sort_by_dict(res['弹簧'], {
        '螺旋弹簧': 0,
        '碟形弹簧': 2,
    }, 'name')

    data = [{'name': '紧固件', 'id': '紧固件', 'children': res['紧固件']}, {'name': '轴承', 'id': '轴承', 'children': res['轴承']},
            {'name': '联轴器', 'id': '联轴器', 'children': res['联轴器']},
            {'name': '弹簧', 'id': '弹簧', 'children': res['弹簧']},
            {'name': '齿轮', 'id': '齿轮', 'children': []},
            # {'name': '液压件', 'id': '液压件', 'children': []},
            ]
    data = [{'name': '高端装备配套常用基础零部件', 'children': data}]

    return data


def get_pro_list(path, page, limit, key):
    """
    获取零件列表
    :param path: 路径列表
    :param page:
    :param limit:
    :param key:
    :return:
    """
    new_path = ['中机数据']
    new_path.extend(path)
    res = get_products(new_path, key)

    res.sort(key=lambda x: _value_opr(x['name']))
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur: (cur + limit)]
    return res, count


def get_products(dirs, key):
    res = []
    _get_products(dirs, res, key)
    return res


def _get_products(dir_list, res, key):
    dir = os.path.join(*dir_list)
    dirs = os.listdir(dir)
    if '3D.stl' in dirs or '2.jpg' in dirs or '2.png' in dirs:
        if key is None:
            res.append({
                'name': dir_list[-1],
                'thumb': '1.jpg',
                'drawing': '2.jpg',
                'path': dir_list
            })
        else:
            if key in dir_list[-1]:
                res.append({
                    'name': dir_list[-1],
                    'thumb': '1.jpg',
                    'drawing': '2.jpg',
                    'path': dir_list
                })
    else:
        for dir_n in dirs:
            new_dir_list = dir_list.copy()
            new_dir_list.append(dir_n)
            _get_products(new_dir_list, res, key)


def _value_opr(value):
    match_obj = re.match(r'[G|J]BT.*?(\d+\.?\d?).*', value)
    if match_obj:
        return float(match_obj.group(1))
    return 200000


def get_technology_quote(path):
    return _get_table_struct('%s%s' % (path, '技术条件和引用标准.xlsx'))


def get_equivalent_head(path):
    res = _get_table_struct(_get_file_path_by_keyword(path, '近似'), 2)
    return res


def get_equivalent_cont(path, limit, page):
    res = _get_table_cont(_get_file_path_by_keyword(path, '近似'), 2)
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur: (cur + limit)]
    return res, count


def get_history_head(path):
    return _get_table_struct('%s%s' % (path, '历年标准.xlsx'), 1)


def get_history_cont(path):
    return _get_table_cont('%s%s' % (path, '历年标准.xlsx'), 1)
