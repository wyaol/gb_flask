import json
from flask import Blueprint
from flask import request
from service import gb_data_service

FILE_NOT_FOUND_CODE = 1
FILE_NOT_FOUND_MSG = '数据文件不存在或格式异常'

SUCCESS_CODE = 0

common = Blueprint('common', __name__)


@common.route('/pro/size_weight_table_head', methods=['POST'])
def size_weight_table_head():
    response = {
        'code': SUCCESS_CODE,
        'msg': '',
        'data': {}
    }
    try:
        prarms = request.get_json()
        path = prarms['path']
        response['data'] = gb_data_service.get_size_weight_table_head(path)
    except FileNotFoundError as e:
        response['code'] = FILE_NOT_FOUND_CODE
        response['msg'] = '%s %s' % (FILE_NOT_FOUND_MSG, str(e))
    finally:
        return json.dumps(response, ensure_ascii=True)


@common.route('/pro/get_size_weight_table_cont', methods=['POST'])
def get_size_weight_table_cont():
    try:
        path = request.form['path']
        limit = request.form['limit']
        page = request.form['page']
        data, count = gb_data_service.get_size_weight_table_cont(path, int(limit), int(page))
        return json.dumps({
            'code': SUCCESS_CODE,
            'msg': '',
            'count': count,
            'data': data
        }, ensure_ascii=True)
    except FileNotFoundError as e:
        print(e)
        return json.dumps({'code': 0, 'msg': FILE_NOT_FOUND_MSG})


@common.route('/pro/tree', methods=['GET'])
def tree():
    return json.dumps(gb_data_service.get_tree(), ensure_ascii=True)


@common.route('/pro/get_pro_list', methods=['POST'])
def get_pro_list():
    id = request.form['id']
    page = request.form['page']
    limit = request.form['limit']
    data, count = gb_data_service.get_pro_list(id, int(page), int(limit))
    return json.dumps({
        'code': SUCCESS_CODE,
        'msg': '',
        'count': count,
        'data': data
    }, ensure_ascii=True)


@common.route('/pro/technology_quote', methods=['POST'])
def technology_quote():
    response = {
        'code': SUCCESS_CODE,
        'msg': '',
        'data': {}
    }
    try:
        path = request.form['path']
        response['data'] = gb_data_service.get_technology_quote(path)
    except FileNotFoundError:
        response['code'] = FILE_NOT_FOUND_CODE
        response['msg'] = '%s %s' % (FILE_NOT_FOUND_MSG)
    finally:
        return json.dumps(response, ensure_ascii=True)


@common.route('/pro/equivalent_head', methods=['POST'])
def equivalent_head():
    response = {
        'code': SUCCESS_CODE,
        'msg': '',
        'data': {}
    }
    try:
        path = request.form['path']
        response['data'] = gb_data_service.get_equivalent_head(path)
    except FileNotFoundError as e:
        response['code'] = FILE_NOT_FOUND_CODE
        response['msg'] = FILE_NOT_FOUND_MSG
    finally:
        return response


@common.route('/pro/equivalent_cont', methods=['POST'])
def equivalent_cont():
    response = {
        'code': SUCCESS_CODE,
        'msg': '',
        'data': {}
    }
    try:
        path = request.form['path']
        limit = request.form['limit']
        page = request.form['page']
        response['data'], response['count'] = gb_data_service.get_equivalent_cont(path, int(limit), int(page))
    except FileNotFoundError as e:
        response['code'] = FILE_NOT_FOUND_CODE
        response['msg'] = FILE_NOT_FOUND_MSG
    finally:
        return response


@common.route('/pro/history_head', methods=['POST'])
def history_head():
    response = {
        'code': SUCCESS_CODE,
        'msg': '',
        'data': {}
    }
    try:
        path = request.form['path']
        response['data'] = gb_data_service.get_history_head(path)
    except FileNotFoundError as e:
        response['code'] = FILE_NOT_FOUND_CODE
        response['msg'] = FILE_NOT_FOUND_MSG
    finally:
        return response

@common.route('/pro/history_cont', methods=['POST'])
def history_cont():
    response = {
        'code': SUCCESS_CODE,
        'msg': '',
        'data': {}
    }
    try:
        path = request.form['path']
        response['data'] = gb_data_service.get_history_cont(path)
    except FileNotFoundError as e:
        response['code'] = FILE_NOT_FOUND_CODE
        response['msg'] = FILE_NOT_FOUND_MSG
    finally:
        return response
