import requests
import random
import datetime
import time
from lxml import etree
import records
import pymysql
from tomorrow import threads
from settings import *

headers = {
    "Proxy-Tunnel": str(random.randint(1, 10000)),
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',

}

db = records.Database('mysql+pymysql://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB))

start_url = 'https://www.qishubook.com'

client = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
cursor = client.cursor()

def create_table_sql(data_dict, table_name):
    """
    generate create sql by dict and table name ,and dict is sorted
    :param data_dict: item dict
    :param table_name:
    """
    ks = data_dict.keys()
    sql = "create table " + table_name + " ("
    sql += "id int(10) not null auto_increment,"
    for each in ks:
        sql += each + " TEXT,"  # each field use text to store
    sql += "primary key (id))"
    return sql

def insert_table_sql(data_dict, table_name):
    """
    generate insert sql by dict and table name ,and dict is sorted
    :param data_dict: item dict
    :param table_name:
    """
    ks = data_dict.keys()
    vs = [data_dict.get(k) if data_dict.get(k) else "" for k in ks]
    sql = "insert into " + table_name + " (" + ",".join(ks) + ") values ("
    for each in vs:
        sql += "'" + pymysql.escape_string(str(each)) + "',"
    sql = sql[:-1] + ")"
    return sql

def data_to_sql(client, cursor, data_dict, table_name):
    insert_sql = insert_table_sql(data_dict, table_name)
    try:
        client.ping(reconnect=True)
        cursor.execute(insert_sql)
        client.commit()
    except Exception as e:
        if "1146" in str(e):
            create_sql = create_table_sql(data_dict, table_name)
            client.ping(reconnect=True)
            cursor.execute(create_sql)
            cursor.execute(insert_sql)
            client.commit()
        else:
            print("Caught PyMysqlError Exception. {}".format(e))
            raise e

def getIp():
    # 代理服务器
    proxyHost = "tps123.kdlapi.com"
    proxyPort = "15818"
    # 代理隧道验证信息
    proxyUser = "t18890465330712"
    proxyPass = "t94bsds3"
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    # 设置 http和https访问都是用HTTP代理
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


def get_resp(url):
    count = 0
    while count < 5:
        count = count + 1
        try:
            resp = requests.get(url, headers=headers, proxies=getIp())
            if resp.status_code == 200:
                resp.encoding = 'gbk'
                return resp.text
        except:
            continue
        time.sleep(1)
    return ''


def parse_fenlei(resp):
    """
        分类页解析
    """
    xml = etree.HTML(resp)
    # 小说列表
    book_list = xml.xpath('//*[@id="mm_14"]/ul/li')
    for book in book_list[1:]:
        # 书名
        book_title = book.xpath('./span[1]/a/text()')
        book_title = ''.join(book_title) if book_title else ''
        # 小说链接
        book_url = book.xpath('./span[1]/a/@href')
        book_url = ''.join(book_url) if book_url else ''
        # 小说id
        book_id = book_url.split('_')[1].replace('/', '')
        # 最新章节名
        new_chart = book.xpath('./span[2]/a/text()')
        new_chart = ''.join(new_chart) if new_chart else ''
        # 最新章节链接
        new_chart_url = book.xpath('./span[2]/a/@href')
        new_chart_url = ''.join(new_chart_url) if new_chart_url else ''
        # 最新章节id
        new_chart_id = new_chart_url.split('/')[-1].replace('.html', '')
        # 作者
        author = book.xpath('./span[3]/text()')
        author = ''.join(author) if author else ''
        print(book_title, book_url, book_id, new_chart, new_chart_url, new_chart_id, author)
        item = {
            'book_title': book_title,
            'book_url': book_url,
            'book_id': int(book_id),
            'new_chart': new_chart,
            'new_chart_url': new_chart_url,
            'new_chart_id': int(new_chart_id),
            'author': author,
        }
        yield item

def parse_next(resp):
    """
        下一页标识解析
    """
    xml = etree.HTML(resp)
    # 下一页标识
    next_page = xml.xpath('//*[@id="mm_14"]//div[@id="pagelink"]/a[last()-2]/text()')
    next_page = ''.join(next_page) if next_page else ''
    return next_page

def get_book_info(url):
    """
        获取小说章节标题及概要
    """
    item = {}
    book_url = start_url + url
    resp = get_resp(book_url)

    xml = etree.HTML(resp)
    # 作者
    # author = xml.xpath('//*[@id="info"]/p[1]/a/text()')
    # author = ''.join(author).strip() if author else ''
    # 书名
    # title = xml.xpath('//*[@id="info"]/h1/text()')
    # title = ''.join(title).strip() if title else ''
    # 图片链接
    img = xml.xpath('//*[@id="fmimg"]/img/@src')
    item['img'] = ''.join(img).strip() if img else 'https://www.qishubook.com/files/article/image/8/8398/8398s.jpg'
    # 小说概要
    abstract = xml.xpath('//*[@id="intro"]//text()')
    item['abstract'] = ''.join(abstract).strip() if abstract else ''
    # 小说章节
    chart = xml.xpath('//li[@class="fenjuan"]')[1]
    chart_url_list = chart.xpath('./following-sibling::li/a/@href')
    # 章节标题
    item['chart_title_list'] = chart.xpath('./following-sibling::li/a/text()')
    # 章节id
    item['chart_id_list'] = [li.replace('.html', '') for li in chart_url_list if li]
    # 列表链接
    item['chart_url_list'] = [url + li for li in chart_url_list if li]

    return item

# get_book_info('/book_112378/')

def get_chart_content(url):
    """
        获取章节内容
    """
    chart_url = start_url + url
    resp = get_resp(chart_url)

    xml = etree.HTML(resp)
    content = xml.xpath('//*[@id="htmlContent"]//text()')
    content = ''.join(content).replace(' 一秒记住【奇书网 www.qishubook.com】，精彩小说无弹窗免费阅读！', '') if content else ''
    print(content)
    return content


# @threads(2)
def update_fenlei(book_cate_num):
    """
        更新分类表: fenlei_table
    """
    page = 1
    update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # update_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    while True:
        page_url = 'https://www.qishubook.com/fenlei/{}_{}/'.format(book_cate_num, page)
        resp = get_resp(page_url)
        if resp:
            next_page = parse_next(resp)

            for item in parse_fenlei(resp):
                item.update({'update_time': update_time})
                if book_cate_num == 1:
                    book_cate = 'xuanhuan'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'xuanhuan'})
                        # 插入分类表
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)
                        print('已更新')

                if book_cate_num == 3:
                    book_cate = 'xianxia'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'xianxia'})
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)

                if book_cate_num == 4:
                    book_cate = 'dushi'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'dushi'})
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)

                if book_cate_num == 5:
                    book_cate = 'lishi'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'lishi'})
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)

                if book_cate_num == 6:
                    book_cate = 'wangyou'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'wangyou'})
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)

                if book_cate_num == 8:
                    book_cate = 'kehuan'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'kehuan'})
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)

                if book_cate_num == 2:
                    book_cate = 'yanqing'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'yanqing'})
                        # 插入分类表
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)

                if book_cate_num == 7:
                    book_cate = 'jingji'
                    book_id_list = query_book_sql(book_cate)
                    # 如果是新书就插入
                    if item['book_id'] not in book_id_list:
                        item.update({'book_cate': 'jingji'})
                        insert_fenlei_table(item)
                    # 更新小说章节
                    new_chart_id = query_chart_sql(item['book_id'], book_cate)
                    if item['new_chart_id'] not in new_chart_id:
                        update_book_sql(item, book_cate)

            if next_page == '>':
                page = page + 1
            else:
                break
        else:
            page = page + 1


def update_info():
    """
        更新小说基本信息表: book_info
        更新小说章节表: book_chart
    """
    query_sql = 'select * from fenlei_table where status=0 limit 2'
    try:
        rows = db.query(query_sql)
    except:
        return update_info()
    for row in rows:
        book_url = row.book_url
        try:
            book_item = get_book_info(book_url)
        except:
            db.query('UPDATE fenlei_table SET status = 2 where book_id=:book_id', **{'book_id': row.book_id})
            continue

        # 小说基本信息表
        book_base = dict(row)
        book_base.update({
            'img': book_item['img'],
            'abstract': book_item['abstract']
        })
        # print(book_base)
        insert_book_info_table(book_base)

        # 小说章节表
        # 章节id
        chart_id_list = book_item['chart_id_list']
        # 列表链接
        chart_url_list = book_item['chart_url_list']
        # 章节标题
        chart_title_list = book_item['chart_title_list']

        for chart_id, chart_url, chart_title in zip(chart_id_list, chart_url_list, chart_title_list):
            chart_item = {
                'book_id': row.book_id,
                'book_title': row.book_title,
                'chart_title': chart_title,
                'chart_id': chart_id,
                'chart_url': chart_url,
                'book_cate': row.book_cate
            }

            insert_chart_table(chart_item)
        db.query('UPDATE fenlei_table SET status = 1 where book_id=:book_id', **{'book_id': row.book_id})

# @threads(2)
def insert_book_info_table(item):
    print(item)
    insert_sql = 'INSERT INTO book_info (book_title, book_url, book_id, new_chart, new_chart_url, new_chart_id, author, update_time, book_cate, abstract, img) ' \
                 'values (:book_title, :book_url, :book_id, :new_chart, :new_chart_url, :new_chart_id, :author, :update_time, :book_cate, :abstract, :img)'
    db.query(insert_sql, **item)

@threads(50)
def insert_chart_table(item):
    """
        插入分类表新的小说
    """
    print(item)
    insert_sql = 'INSERT INTO book_chart (book_title, book_id, chart_title, chart_id, chart_url) ' \
                 'values (:book_title, :book_id, :chart_title, :chart_id, :chart_url)'
    db.query(insert_sql, **item)




def insert_fenlei_table(item):
    """
        插入分类表新的小说
    """
    insert_sql = 'INSERT INTO fenlei_table (book_title, book_url, book_id, new_chart, new_chart_url, new_chart_id, author, update_time, book_cate) ' \
                 'values (:book_title, :book_url, :book_id, :new_chart, :new_chart_url, :new_chart_id, :author, :update_time, :book_cate)'
    db.query(insert_sql, **item)


def update_book_sql(item, book_cate):
    """
        更新分类表的小说
    """
    emp = {
        'new_chart_url': item['new_chart_url'],
        'new_chart_id': item['new_chart_id'],
        'new_chart': item['new_chart'],
        'update_time': item['update_time'],
        'book_cate': book_cate,
        'book_id': item['book_id']
    }
    update_book_sql = 'update fenlei_table set new_chart=:new_chart,new_chart_id=:new_chart_id,new_chart_url=:new_chart_url,update_time=:update_time where book_id=:book_id and book_cate=:book_cate'
    db.query(update_book_sql, **emp)


def query_book_sql(book_cate):
    """
        查询分类表小说id
    """
    emp = {
        'book_cate': book_cate
    }
    book_id_list = []
    query_sql = 'select book_id from fenlei_table where book_cate=:book_cate'
    try:
        rows = db.query(query_sql, **emp)
    except:
        return query_book_sql(book_cate)
    for row in rows:
        book_id_list.append(row.book_id)
    # print(book_id_list)
    return book_id_list
# query_book_sql('kehuan')

def query_chart_sql(book_id, book_cate):
    """
        查询分类表小说章节id
    """
    emp = {
        'book_cate': book_cate,
        'book_id': book_id
    }
    chart_id_list = []
    query_sql = 'select new_chart_id from fenlei_table where book_id=:book_id and book_cate=:book_cate'
    try:
        rows = db.query(query_sql, **emp)
    except:
        return query_chart_sql(book_id, book_cate)
    for row in rows:
        chart_id_list.append(row.new_chart_id)
    return chart_id_list



while True:
    update_info()

# update_fenlei(1)

# item = {
#     'new_chart_url': '/book_76312/51024418.html',
#     'new_chart_id': 51024418,
#     'new_chart': '第5203章 全年碾压，暴揍姬赢！',
#     'update_time': '2020-10-27 19:31:00',
#     'book_id': '76312',
# }
# update_book_sql(item, 'xuanhuan')
# query_chart_sql('89915', 'xuanhuan')

# for i in [2, 3, 4, 5, 6, 7, 8]:
# insert_fenlei(6)


# parse_fenlei(get_resp('https://www.qishubook.com/fenlei/1_1/'))
# get_chart_content('/book_108237/50979292.html')
# get_book_info('/book_108237/')
