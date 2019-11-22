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

    if head_line is None: head_line = row_num

    for i in range(head_line):
        row = []
        for j in range(col_num):
            value = table.cell(i, j).value
            if value == '':
                continue
            item = {'title': value}

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
            row[str(i)] = cols[i]
        res.append(row)
    return res

def get_size_weight_table_head(path):
    return _get_table_struct(_get_file_path_by_keyword(path, '尺寸'), 2)


def get_size_weight_table_cont(path, limit, page):
    res = _get_table_cont(_get_file_path_by_keyword(path, '尺寸'))
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur: (cur + limit)]
    return res, count


def get_tree():
    res = []
    dirs = os.listdir('中机数据/')
    for i in range(len(dirs)):
        res.append({'pId': '111', 'id': dirs[i], 'name': dirs[i]})

    data = [{'name': '全部', 'id': '全部', 'children': [{'name': '通用零部件', 'children': [{'name': '紧固件', 'children': res}]},
                                        {'name': '轴承、齿轮、和传动部件'}]}]

    return data

def get_pro_list(id, page, limit):
    """
    获取标准列表
    :param id: 标准大类名称
    :return:
    """
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
    count = len(res)
    cur = (page - 1) * limit
    res = res[cur : (cur + limit)]
    return res, count

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