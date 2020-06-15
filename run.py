import os
from flask import Flask, Response, send_file, make_response
from flask_cors import CORS
from controller import example_controller, common_controller

app = Flask(__name__)
app.register_blueprint(example_controller.example)
app.register_blueprint(common_controller.common)


@app.route("/中机数据/<category>/<obj>/<name>/<img_name>")
def index(category, obj, name, img_name):
    if 'stl' in img_name:
        return send_file('中机数据/%s/%s/%s/%s' % (category, obj, name, img_name))
    elif 'xlsx' in img_name:
        path = '中机数据/%s/%s/%s/%s' % (category, obj, name, img_name)
        with open(path, 'rb') as f:
            excel = f.read()
        # resp = Response(excel, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        #     headers={
        #         'Access-Control-Allow-Origin': '*',
        #         'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        #     }
        # )
        res = make_response(excel)
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Method'] = 'GET, POST, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = '*'
        res.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return res
    else:
        img_path1 = '中机数据/%s/%s/%s/%s.jpg' % (category, obj, name, img_name)
        img_path2 = '中机数据/%s/%s/%s/%s.png' % (category, obj, name, img_name)
        if os.path.exists(img_path1) is False and os.path.exists(img_path2) is False: return ''
        elif os.path.exists(img_path1) is True:img_path = img_path1
        else: img_path = img_path2
        with open(img_path, 'rb') as f:
            image = f.read()
        resp = Response(image, mimetype="image/jpeg")
        return resp


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(host="0.0.0.0", port=8015, debug=True)