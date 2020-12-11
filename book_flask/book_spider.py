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
    while count < 10:
        count = count + 1
        try:
            resp = requests.get(url, headers=headers, proxies=getIp())
            if resp.status_code == 200:
                # resp.encoding = 'utf-8'
                return resp.text
            else:
                continue
        except:
            print('-----{}---requests error--------'.format(url))
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
        # print(book_title, book_url, book_id, new_chart, new_chart_url, new_chart_id, author)
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

    # 图片链接
    img = xml.xpath('//*[@id="fmimg"]/img/@src')
    item['img'] = ''.join(img).strip() if img else 'https://www.qishubook.com/files/article/image/8/8398/8398s.jpg'
    # 小说概要
    abstract = xml.xpath('//*[@id="intro"]//text()')
    item['abstract'] = ''.join(abstract).strip() if abstract else ''
    # 小说章节
    # try:
    # chart = xml.xpath('//li[@class="fenjuan"]')[1]
    chart = xml.xpath('//ul[@class="mulu_list"]/div[@class="clear"]')[0]
    # except:
        # chart = xml.xpath('//ul[@class="mulu_list"]/div[@class="clear"]')[0]
    chart_url_list = chart.xpath('./following-sibling::li/a/@href')
    # 章节标题
    item['chart_title_list'] = chart.xpath('./following-sibling::li/a/text()')
    # 章节id
    item['chart_id_list'] = [li.replace('.html', '') for li in chart_url_list if li]
    # 链接列表
    item['chart_url_list'] = [url + li for li in chart_url_list if li]
    # print(item['chart_title_list'])
    return item

# get_book_info('/book_126710/')

def get_chart_content(url):
    """
        获取章节内容
    """
    chart_url = start_url + url
    resp = get_resp(chart_url)

    xml = etree.HTML(resp)
    content = xml.xpath('//*[@id="htmlContent"]//text()')
    content = ''.join(content).replace('一秒记住【奇书网 www.qishubook.com】，精彩小说无弹窗免费阅读！', '') if content else ''
    # print(content)
    return content
# get_chart_content('/book_30871/12044679.html')

def load_chart_content(start_id):
    """
        下载小说章节
    """
    query_sql = 'select * from book_chart_copy2'
    try:
        rows = db.query(query_sql)
    except:
        return load_chart_content(start_id)
    for row in rows:
        try:
            insert_chart_content_table(row)
        except Exception as e:
            print('-----------sql error !----{}------'.format(e))
            continue


# @threads(2)
def update_fenlei(book_cate_num):
    """
        更新分类表和章节表: book_info、book_chart
    """
    page = 1
    # update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # update_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    while True:
        print('--------page--{}-------'.format(page))
        page_url = 'https://www.qishubook.com/fenlei/{}_{}/'.format(book_cate_num, page)
        resp = get_resp(page_url)
        if resp:
            next_page = parse_next(resp)

            for item in parse_fenlei(resp):
                process_book(item, book_cate_num)

            if next_page == '>':
                page = page + 1
            else:
                break
        else:
            page = page + 1

@threads(10)
def process_book(item, book_cate_num):
    """子进程"""
    print(item)
    item.update({'update_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
    if book_cate_num == 1:
        book_cate = 'xuanhuan'
    elif book_cate_num == 2:
        book_cate = 'yanqing'
    elif book_cate_num == 3:
        book_cate = 'xianxia'
    elif book_cate_num == 4:
        book_cate = 'dushi'
    elif book_cate_num == 5:
        book_cate = 'lishi'
    elif book_cate_num == 6:
        book_cate = 'wangyou'
    elif book_cate_num == 7:
        book_cate = 'jingji'
    elif book_cate_num == 8:
        book_cate = 'kehuan'
    else:
        book_cate = ''

    book_id_list = query_book_sql(book_cate)
    # 如果是新书就插入
    if int(item['book_id']) not in book_id_list:
        # 获取小说简介和章节列表
        book_url = item['book_url']
        book_info_item = get_book_info(book_url)
        img = book_info_item['img']
        abstract = book_info_item['abstract']
        chart_title_list = book_info_item['chart_title_list']
        chart_id_list = book_info_item['chart_id_list']
        chart_url_list = book_info_item['chart_url_list']

        # 插入分类表: book_info
        item.update({'img': img, 'abstract': abstract, 'book_cate': 'xuanhuan'})
        insert_fenlei_table(item)
        # 插入章节表: book_chart
        for chart_id, chart_url, chart_title in zip(chart_id_list, chart_url_list, chart_title_list):
            chart_item = {
                'book_id': item['book_id'],
                'book_title': item['book_title'],
                'chart_title': chart_title,
                'chart_id': chart_id,
                'chart_url': chart_url,
            }
            insert_chart_table(chart_item)

    # 如果已经有该小说，则更新小说章节
    else:
        new_chart_id = query_new_chart_sql(item['book_id'], book_cate)
        if int(item['new_chart_id']) not in new_chart_id:
            # 更新小说分类表：book_info
            update_book_sql(item, book_cate)
            # 更新小说章节列表
            # 获取小说章节列表
            book_url = item['book_url']
            book_info_item = get_book_info(book_url)
            chart_title_list = book_info_item['chart_title_list']
            chart_id_list = book_info_item['chart_id_list']
            chart_url_list = book_info_item['chart_url_list']

            query_id_list = query_chart_sql(item['book_id'])
            # 插入章节表: book_chart
            for chart_id, chart_url, chart_title in zip(chart_id_list, chart_url_list, chart_title_list):
                if int(chart_id) not in query_id_list:
                    chart_item = {
                        'book_id': item['book_id'],
                        'book_title': item['book_title'],
                        'chart_title': chart_title,
                        'chart_id': chart_id,
                        'chart_url': chart_url,
                    }
                    insert_chart_table(chart_item)


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


# @threads(50)
def insert_chart_content_table(row):
    """
        插入章节表
    """
    chart_url = row.chart_url
    chart_content = get_chart_content(chart_url)

    # 小说章节表
    chart_base = {
        'book_id': row.book_id,
        'book_title': row.book_title,
        'chart_title': row.chart_title,
        'chart_id': row.chart_id,
        'chart_content': chart_content,
    }
    print(row.book_title)
    insert_sql = 'INSERT INTO book_chart_content (book_title, book_id, chart_title, chart_id, chart_content) ' \
                 'values (:book_title, :book_id, :chart_title, :chart_id, :chart_content)'
    db.query(insert_sql, **chart_base)

# load_chart_content()

# @threads(50)
def insert_chart_table(item):
    """
        插入新的小说: book_chart表
    """
    print(item)
    insert_sql = 'INSERT INTO book_chart (book_title, book_id, chart_title, chart_id, chart_url) ' \
                 'values (:book_title, :book_id, :chart_title, :chart_id, :chart_url)'
    db.query(insert_sql, **item)


def insert_fenlei_table(item):
    """
        插入新的小说: book_info表
    """
    insert_sql = 'INSERT INTO book_info (book_title, book_url, book_id, new_chart, new_chart_url, new_chart_id, author, update_time, book_cate, img, abstract) ' \
                 'values (:book_title, :book_url, :book_id, :new_chart, :new_chart_url, :new_chart_id, :author, :update_time, :book_cate, :img, :abstract)'
    db.query(insert_sql, **item)


def update_book_sql(item, book_cate):
    """
        更新小说: book_info表
    """
    emp = {
        'new_chart_url': item['new_chart_url'],
        'new_chart_id': item['new_chart_id'],
        'new_chart': item['new_chart'],
        'update_time': item['update_time'],
        'book_cate': book_cate,
        'book_id': item['book_id']
    }
    update_book_sql = 'update book_info set new_chart=:new_chart,new_chart_id=:new_chart_id,new_chart_url=:new_chart_url,update_time=:update_time where book_id=:book_id and book_cate=:book_cate'
    db.query(update_book_sql, **emp)


def query_book_sql(book_cate):
    """
        查询分类表小说id: book_info表
    """
    emp = {
        'book_cate': book_cate
    }
    book_id_list = []
    query_sql = 'select book_id from book_info where book_cate=:book_cate'
    try:
        rows = db.query(query_sql, **emp)
    except:
        return query_book_sql(book_cate)
    for row in rows:
        book_id_list.append(row.book_id)
    # print(book_id_list)
    return book_id_list
# query_book_sql('kehuan')

def query_new_chart_sql(book_id, book_cate):
    """
        查询分类表小说最新章节id: book_info表
    """
    emp = {
        'book_cate': book_cate,
        'book_id': book_id
    }
    chart_id_list = []
    query_sql = 'select new_chart_id from book_info where book_id=:book_id and book_cate=:book_cate'
    try:
        rows = db.query(query_sql, **emp)
    except:
        return query_new_chart_sql(book_id, book_cate)
    for row in rows:
        chart_id_list.append(row.new_chart_id)
    return chart_id_list


def query_chart_sql(book_id):
    """
        查询分类表小说所有章节id: book_chart表
    """
    emp = {
        'book_id': book_id
    }
    chart_id_list = []
    query_sql = 'select chart_id from book_chart where book_id=:book_id'
    try:
        rows = db.query(query_sql, **emp)
    except:
        return query_chart_sql(book_id)
    for row in rows:
        chart_id_list.append(row.chart_id)
    # print(chart_id_list)
    return chart_id_list

# query_chart_sql('1318')

# load_chart_content(0)
# start_id = 0
# while start_id < 1000000:
#     load_chart_content(start_id)
#     start_id = start_id + 1000

# update_fenlei(6)

def addition_book_chart(book_id):
    """
        补充缺失章节的小说
    """
    url = '/book_{}/'.format(book_id)
    book_url = start_url + url
    resp = get_resp(book_url)

    xml = etree.HTML(resp)
    # 小说标题
    book_title = xml.xpath('//div[@id="info"]/h1/text()')
    book_title = ''.join(book_title)
    # 小说章节
    chart = xml.xpath('//ul[@class="mulu_list"]/div[@class="clear"]')[0]
    # chart = xml.xpath('//ul[@class="mulu_list"]/div[@class="clear"]')[0]
    chart_url_list = chart.xpath('./following-sibling::li/a/@href')
    # 章节标题
    chart_title_list = chart.xpath('./following-sibling::li/a/text()')
    # 章节id
    chart_id_list = [li.replace('.html', '') for li in chart_url_list if li]
    # 链接列表
    chart_url_list = [url + li for li in chart_url_list if li]
    # print(item['chart_title_list'])

    query_id_list = query_chart_sql(book_id)

    emp = {
        'book_id': book_id
    }
    query_sql = 'select chart_id from book_chart_content where book_id=:book_id'
    rows = db.query(query_sql, **emp)
    chart_content_list = []
    for row in rows:
        chart_content_list.append(row.chart_id)
    print(chart_content_list)
    for chart_title, chart_id, chart_url in zip(chart_title_list, chart_id_list, chart_url_list):
        if int(chart_id) not in query_id_list:
            chart_item = {
                'book_id': book_id,
                'book_title': book_title,
                'chart_title': chart_title,
                'chart_id': chart_id,
                'chart_url': chart_url,
            }
            insert_chart_table(chart_item)

        if int(chart_id) not in chart_content_list:
            chart_content = get_chart_content(chart_url)

            # 小说章节表
            chart_base = {
                'book_id': book_id,
                'book_title': book_title,
                'chart_title': chart_title,
                'chart_id': chart_id,
                'chart_content': chart_content,
            }
            print(chart_title)
            insert_sql = 'INSERT INTO book_chart_content (book_title, book_id, chart_title, chart_id, chart_content) ' \
                         'values (:book_title, :book_id, :chart_title, :chart_id, :chart_content)'
            db.query(insert_sql, **chart_base)

addition_book_chart(27835)
