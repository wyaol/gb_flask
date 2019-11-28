import xlrd
import os
from utils.common_utils import dict_add


def _get_filename_by_partname(chooses, partname):
    for choose in chooses:
        if partname in choose: return choose
    return None


def _get_file_path_by_keyword(path, keyword):
    files = os.listdir(path)
    choose = _get_filename_by_partname(files, keyword)
    if choose is None: raise FileNotFoundError()
    return '%s%s' % (path, choose)


def _get_table_struct(path, head_line=None):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    row_num = table.nrows
    col_num = table.ncols

    res = []
    history = []

    #计算每列的长度
    col_word_count_max = [0] * col_num
    for i in range(col_num):
        for j in range(row_num):
            value = table.cell(j, i).value
            count = len(str(value)) // 2 if type(value) is float else len(value)
            col_word_count_max[i] = col_word_count_max[i] if count < col_word_count_max[i] else count

    if head_line is None: head_line = row_num

    for i in range(head_line):
        row = []
        for j in range(col_num):
            value = table.cell(i, j).value
            if value == '':
                continue
            item = {'title': value}

            item['width'] = col_word_count_max[j] * 20 + 20
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

def _get_table_data(path, head_line=None):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    row_num = table.nrows
    col_num = table.ncols
    res = []
    if head_line is None: head_line = 0
    for i in range(head_line, row_num):
        row = []
        for j in range(col_num):
            row.append(table.cell(i, j).value)
        res.append(row)
    return res

def _get_table_cont(path, head_line=None):
    res_array = _get_table_data(path, head_line)
    res = []
    for cols in res_array:
        row = {}
        for i in range(len(cols)):
            value = cols[i]
            row[str(i)] = value if type(value) is not float else round(value, 3)
        res.append(row)
    return res

def get_size_weight_table_head(path):
    if '自攻螺钉' in path:
        line = 3
    else: line = 2

    return _get_table_struct(_get_file_path_by_keyword(path, '尺寸'), line)


def get_size_weight_table_cont(path, limit, page):
    if '自攻螺钉' in path:
        line = 3
    else: line = 2

    res = _get_table_cont(_get_file_path_by_keyword(path, '尺寸'), line)
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur: (cur + limit)]
    return res, count


def get_tree():
    res = []
    dirs = os.listdir('中机数据/')
    for i in range(len(dirs)):
        res.append({'pId': '111', 'id': dirs[i], 'name': dirs[i]})

    data = [{'name': '全部', 'children': [{'name': '通用零部件', 'children': [{'name': '紧固件', 'children': res}]},
                                        {'name': '轴承、齿轮、和传动部件'}]}]

    return data

def get_pro_list(id, page, limit, key):
    """
    获取标准列表
    :param id: 标准大类名称
    :return:
    """
    if id is None and key is None:
        res = _get_pro_list_by_key('')
    elif key is not None and id is None:
        res = _get_pro_list_by_key(key)
    elif key is not None and id is not None:
        res = _get_pro_list_by_key_id(key, id)
    else:
        res = _get_pro_list_by_id(id)
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur : (cur + limit)]
    return res, count

def _get_pro_list_by_id(id):
    res = []
    dir_parent = '中机数据/%s/' % id
    dirs = os.listdir(dir_parent)

    for dir in dirs:
        res.append({
            'name': dir,
            'thumb': '1',
            'drawing': '2',
            'path': '%s%s/' % (dir_parent, dir)
        })
    return res

def _get_pro_list_by_key(key):
    res = []
    dir_parent = '中机数据'
    dirss = os.listdir(dir_parent)
    for dirs in dirss:
        dir_next = os.listdir('%s/%s/' % (dir_parent, dirs))
        for dir in dir_next:
            if key not in dir: continue
            res.append({
                'name': dir,
                'thumb': '1',
                'drawing': '2',
                'path': '%s/%s/%s/' % (dir_parent, dirs, dir)
            })
    return res

def _get_pro_list_by_key_id(key, id):
    res = []
    dir_parent = '中机数据'
    dirs = os.listdir('%s/%s/' % (dir_parent, id))
    for dir in dirs:
        if key not in dir: continue
        res.append({
            'name': dir,
            'thumb': '1',
            'drawing': '2',
            'path': '%s/%s/%s/' % (dir_parent, id, dir)
            })
    return res

def get_technology_quote(path):
    return  _get_table_struct('%s%s' % (path, '技术条件和引用标准.xlsx'))

def get_equivalent_head(path):
    res = _get_table_struct(_get_file_path_by_keyword(path, '近似'), 1)
    return res

def get_equivalent_cont(path, limit, page):
    res = _get_table_cont(_get_file_path_by_keyword(path, '近似'), 1)
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur: (cur + limit)]
    return res, count

def get_history_head(path):
    return  _get_table_struct('%s%s' % (path, '历史标准.xlsx'), 1)

def get_history_cont(path):
    return _get_table_cont('%s%s' % (path, '历史标准.xlsx'), 1)