import records
from settings import *

class Books(object):

    def __init__(self):
        self.db = records.Database('mysql+pymysql://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB))

    def search_infos_by_key(self, key):
        emp = {
            'book_title': key,
            'author': key
        }
        sql = "select * from fenlei_table where book_title=:book_title or author=:author"
        rows = self.db.query(sql, **emp)
        data = []
        for row in rows:
            data.append(row.as_dict())
        # print(data)
        return data

    def get_book_info_limit(self):
        """

        :return:
        """
        book_list = []
        sql = 'select * from fenlei_table limit 5'
        rows = self.db.query(sql)
        for row in rows:
            book_list.append(row.as_dict())
        return book_list

    def get_cates_newst_books_30(self, book_cate):
        # sql = "select id, book_name,book_id,book_last_update_time, \
        # book_newest_name,book_newest_url from book_infos \
        # where book_cate='{}' order by book_last_update_time desc limit 30;".format(book_cate)
        book_list = []
        emp = {
            'book_cate': book_cate,
        }
        sql = 'select * from fenlei_table where book_cate=:book_cate limit 20'
        rows = self.db.query(sql, **emp)
        for row in rows:
            book_list.append(row.as_dict())
        return book_list

    def get_cates_most_books_30(self, book_cate):
        book_list = []
        emp = {
            'book_cate': book_cate,
        }
        sql = 'select * from fenlei_table where book_cate=:book_cate limit 20'
        rows = self.db.query(sql, **emp)
        for row in rows:
            book_list.append(row.as_dict())
        return book_list

    def get_book_infos_by_book_id(self, book_id):
        """
            查询小说简介
        """
        data = []
        emp = {
            'book_id': book_id,
        }
        sql = "select * from book_info where book_id=:book_id"
        rows = self.db.query(sql, **emp)
        for row in rows:
            data.append(row.as_dict())
        return data

    def get_book_all_caps_by_book_id(self,book_id):
        """
            查询小说所有章节列表
        """
        data = []
        emp = {
            'book_id': book_id,
        }
        sql = "select book_id,chart_id,chart_title from book_chart where book_id=:book_id order by chart_id"
        rows = self.db.query(sql, **emp)
        for row in rows:
            data.append(row.as_dict())
        return data


    def get_book_newest_20_caps_by_book_id(self,book_id):
        """
            查询小说最新的章节列表
        """
        data = []
        emp = {
            'book_id': book_id,
        }        
        sql = "select book_id,chart_id,chart_title from book_chart where book_id=:book_id order by chart_id desc limit 20"
        rows = self.db.query(sql, **emp)
        for row in rows:
            data.append(row.as_dict())
        return data



if __name__ == '__main__':
    books = Books()
    books.get_book_infos_by_book_id(30571)