from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
from books import Books
import json
import re
import time
import rsa
import base64
from settings import RSA_1024_PRIV_KEY, BOOK_LIST

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello_world():
    books = Books()
    sql_data = books.get_book_info_limit()
    resData = {
        "resCode": 0,  # 非0即错误 1
        "data": sql_data,  # 数据位置，一般为数组
        "message": '图书的信息'
    }
    return jsonify(resData)


@app.route('/books_cates', methods=['GET'])
def get_books_cates():
    resData = {
        "resCode": 0, # 非0即错误 1
        "data": [
            {"id":0, "text": '首页', "url":'/'},
            {"id":1, "text": '玄幻', "url":'/xuanhuan'},
            {"id":2, "text": '仙侠', "url":'/xianxia'},
            {"id":3, "text": '都市', "url":'/dushi'},
            {"id":4, "text": '历史', "url":'/lishi'},
            {"id":5, "text": '网游', "url":'/wangyou'},
            {"id":6, "text": '科幻', "url":'/kehuan'},
            {"id":7, "text": '言情', "url":'/yanqing'},
            {"id":8, "text": '竞技', "url":'/jingji'},
            {"id":9, "text": '完本', "url":'/quanben'},
        ],# 数据位置，一般为数组
        "message": '对本次请求的说明'
    }
    return jsonify(resData)

# 搜索接口
@app.route('/search', methods=['POST'])
def search_infos():
    if request.method == 'POST':
        get_data = json.loads(request.get_data(as_text=True))
        key = get_data['key']
        # key = request.form.get('key')
        print(key)
        # secretKey = get_data['secretKey']
        # secret_result = get_secret_key(secretKey)
        # if secret_result['request_time'] == '':
        #     # 如果这边返回的是空的，说明请求的数据已经被破坏了
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        # if is_allow_domain_time(secret_result['request_time'], secret_result['request_url']):
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        # if is_string_validate(key):
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '参数错误'
        #     }
        #     return jsonify(resData)
        books = Books()
        search_data = books.search_infos_by_key(key)
        print(search_data)
        if len(search_data) == 0:
            resData = {
                "resCode": 0, # 非0即错误 1
                "data": [],# 数据位置，一般为数组
                "message": '数据为空'
            }
            return jsonify(resData)

        resData = {
            "resCode": 0, # 非0即错误 1
            "data": search_data,# 数据位置，一般为数组
            "message": '搜索结果'
        }
        return jsonify(resData)
    else:
        resData = {
            "resCode": 1, # 非0即错误 1
            "data": [],# 数据位置，一般为数组
            "message": '请求方法错误'
        }
        return jsonify(resData)

@app.route('/<string:book_cate>', methods=['POST'])
def get_cates_infos(book_cate):
    if is_string_validate(book_cate):
        print("输入数据有错误")
        resData = {
            "resCode": 404, # 非0即错误 1
            "data": [],# 数据位置，一般为数组
            "message": '输入数据有错误'
        }
        return jsonify(resData)

    if request.method == 'POST':
        print("捕获到了post请求 book_cate", book_cate)
        get_data = json.loads(request.get_data(as_text=True))
        key = get_data['key']
        print("key = ", key)
        # secretKey = get_data['secretKey']
        # secret_result = get_secret_key(secretKey)
        # if secret_result['request_time'] == '':
        #     # 如果这边返回的是空的，说明请求的数据已经被破坏了
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        # if is_allow_domain_time(secret_result['request_time'], secret_result['request_url']):
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        if book_cate in BOOK_LIST:
            print(key, " is in BOOK_LIST")
            # print(key, secretKey)
            if key == 'newest':
                # select * from book_infos where book_cate='xiuzhen' order by book_last_update_time desc limit 3
                print("newest")
                books = Books()
                sql_data = books.get_cates_newst_books_30(book_cate)
                resData = {
                    "resCode": 0, # 非0即错误 1
                    "data": sql_data,# 数据位置，一般为数组
                    "message": '最新的30本图书信息查询结果'
                }
                return jsonify(resData)
            elif key == 'most':
                print("most")
                books = Books()
                sql_data = books.get_cates_most_books_30(book_cate)
                resData = {
                    "resCode": 0, # 非0即错误 1
                    "data": sql_data,# 数据位置，一般为数组
                    "message": '最多的30本图书信息查询结果'
                }
                return jsonify(resData)

            else:
                resData = {
                    "resCode": 2, # 非0即错误 1
                    "data": [],# 数据位置，一般为数组
                    "message": '参数有误'
                }
                return jsonify(resData)
        else:
            print("key is not BOOK_LIST")
            return 404
    else:
        resData = {
            "resCode": 1, # 非0即错误 1
            "data": [],# 数据位置，一般为数组
            "message": '请求方法错误'
        }
        return jsonify(resData)

# 图书首页信息
@app.route('/book/<int:book_id>', methods=['POST'])
def get_book_infos_by_id(book_id):
    if request.method == 'POST':
        get_data = json.loads(request.get_data(as_text=True))
        key = get_data['key']
        # secretKey = get_data['secretKey']
        # secret_result = get_secret_key(secretKey)
        # if secret_result['request_time'] == '':
            # 如果这边返回的是空的，说明请求的数据已经被破坏了
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        # if is_allow_domain_time(secret_result['request_time'], secret_result['request_url']):
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        books = Books()
        sql_data = books.get_book_infos_by_book_id(book_id)
        if key == 'index':
            resData = {
                "resCode": 0, # 非0即错误 1
                "data": sql_data,# 数据位置，一般为数组
                "message": '图书的信息'
            }
            return jsonify(resData)
        elif key == "cap20":
            if len(sql_data) == 0:
                resData = {
                    "resCode": 5, # 非0即错误 1
                    "data": [],# 数据位置，一般为数组
                    "message": '图书不存在'
                }
                return jsonify(resData)
            cap_20_data = books.get_book_newest_20_caps_by_book_id(book_id)
            resData = {
                "resCode": 0, # 非0即错误 1
                "data": cap_20_data,# 数据位置，一般为数组
                "message": '最新的20章内容'
            }
            return jsonify(resData)
        elif key == "all":
            if len(sql_data) == 0:
                resData = {
                    "resCode": 5, # 非0即错误 1
                    "data": [],# 数据位置，一般为数组
                    "message": '图书不存在'
                }
                return jsonify(resData)
            all_cap_data = books.get_book_all_caps_by_book_id(book_id)
            resData = {
                "resCode": 0, # 非0即错误 1
                "data": all_cap_data,# 数据位置，一般为数组
                "message": '所有图书信息'
            }
            return jsonify(resData)
        else:
            resData = {
                "resCode": 1, # 非0即错误 1
                "data": [],# 数据位置，一般为数组
                "message": '参数错误'
            }
            return jsonify(resData)
        # book_infos
    else:
        resData = {
            "resCode": 1, # 非0即错误 1
            "data": [],# 数据位置，一般为数组
            "message": '请求方法错误'
        }
        return jsonify(resData)

# 获取图书详情页接口
@app.route('/book/<int:book_id>/<int:sort_id>', methods=['POST'])
def get_book_detail_infos(book_id, sort_id):
    if request.method == 'POST':
        # get_data = json.loads(request.get_data(as_text=True))
        # secretKey = get_data['secretKey']
        # secret_result = get_secret_key(secretKey)
        # if secret_result['request_time'] == '':
        #     # 如果这边返回的是空的，说明请求的数据已经被破坏了
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        # if is_allow_domain_time(secret_result['request_time'], secret_result['request_url']):
        #     resData = {
        #         "resCode": 1, # 非0即错误 1
        #         "data": [],# 数据位置，一般为数组
        #         "message": '你猜，你使劲猜'
        #     }
        #     return jsonify(resData)
        book = Books()
        sql_book_id_data = book.get_book_infos_by_book_id(book_id)
        if len(sql_book_id_data) == 0:
            # 不存在该图书
            resData = {
                "resCode": 1, # 非0即错误 1
                "data": [],# 数据位置，一般为数组
                "message": '不存在该图书信息'
            }
            return jsonify(resData)
        # 该图书存在
        # print("sql_book_id_data[0]['book_name'] = ", sql_book_id_data[0]['book_name'])
        sql_detail_data = book.get_book_detail_by_book_id_sort_id(book_id, sort_id)

        next_data = book.get_next_cap_id(book_id, sort_id)
        print("in flask :next_data = ", next_data)
        if next_data == None:
            print("next_data == None")
            sql_detail_data[0]['next_sort_id'] = ''
        else:
            print("next_data != None")
            sql_detail_data[0]['next_sort_id'] = next_data['chart_id']

        before_data = book.get_before_cap_id(book_id, sort_id)
        if before_data == None:
            print("before_data == None")
            sql_detail_data[0]['before_sort_id'] = ''
        else:
            sql_detail_data[0]['before_sort_id'] = before_data['chart_id']


        sql_detail_data[0]['book_title'] = sql_book_id_data[0]['book_title']


        resData = {
            "resCode": 0, # 非0即错误 1
            "data": sql_detail_data,# 数据位置，一般为数组
            "message": '所有图书信息'
        }
        return jsonify(resData)
    else:
        resData = {
            "resCode": 1, # 非0即错误 1
            "data": [],# 数据位置，一般为数组
            "message": '请求方法错误'
        }
        return jsonify(resData)

# 解密函数
def get_secret_key(cryptdata):
    # print("cryptdata = ", cryptdata)
    privkey = rsa.PrivateKey.load_pkcs1(RSA_1024_PRIV_KEY)
    msg = rsa.decrypt(base64.b64decode(cryptdata), privkey)
    # msg = rsa.decrypt(base64.b64decode(cryptdata), RSA_1024_PRIV_KEY)
    # print("str(msg) = ", msg)
    # print("str(msg) = ", msg.decode().split(":")[1])
    try:
        result = {
            "request_time":msg.decode().split(":")[0],  # 防止爬虫利用这个反复爬取
            "request_url":msg.decode().split(":")[1],
            "request_infos": msg.decode().split(":")[2]
        }
    except:
        result = {
            "request_time":'',  # 防止爬虫利用这个反复爬取
            "request_url":'',
            "request_infos": ''
        }
    # print("result = ", result)
    return result

def is_allow_domain_time(request_time, request_url):
    if(int(time.time() * 1000) - int(request_time) > 300000):
        # 一个加密数据只能在3W毫秒之内访问
        # resData = {
        #     "resCode": 1, # 非0即错误 1
        #     "data": [],# 数据位置，一般为数组
        #     "message": '你猜，你使劲猜'
        # }
        # return jsonify(resData)
        return True

# 检查是否含有特殊字符
def is_string_validate(str):
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",str)
    if len(str) == len(sub_str):
        # 说明合法
        return False
    else:
        # 不合法
        return True

if __name__ == '__main__':
    # print(app.url_map)
    app.run()
