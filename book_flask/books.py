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
        sql = "select * from book_info where book_title=:book_title or author=:author"
        rows = self.db.query(sql, **emp)
        data = []
        for row in rows:
            data.append(row.as_dict())
        # print(data)
        return data

    def get_book_info_limit(self):
        """
            首页热门推荐
        """
        book_list = []
        sql = 'select * from book_info limit 6'
        rows = self.db.query(sql)
        for row in rows:
            book_list.append(row.as_dict())
        # print(book_list)
        return book_list

    def get_cates_newst_books_30(self, book_cate):
        """
            查询各分类的最新更新的小说
        """
        book_list = []
        emp = {
            'book_cate': book_cate,
        }
        sql = 'select * from book_info where book_cate=:book_cate limit 20'
        rows = self.db.query(sql, **emp)
        for row in rows:
            book_list.append(row.as_dict())
        return book_list

    def get_cates_most_books_30(self, book_cate):
        """
            查询各分类的最多的小说
        """
        book_list = []
        emp = {
            'book_cate': book_cate,
        }
        sql = 'select * from book_info where book_cate=:book_cate limit 20'
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

    def get_book_detail_by_book_id_sort_id(self, book_id, chart_id):
        data = []
        emp = {
            'book_id': book_id,
            'chart_id': chart_id,
        }
        sql = "select * from book_chart_content where book_id=:book_id and chart_id=:chart_id;"
        rows = self.db.query(sql, **emp)
        for row in rows:
            data.append(row.as_dict())
        return data

    # 查询下一章的sql： select * from book_details where book_id=45563 and sort_id>328922 order by sort_id  limit 1
    def get_next_cap_id(self, book_id, chart_id):
        data = []
        emp = {
            'book_id': book_id,
            'chart_id': chart_id,
        }
        sql = "select chart_id from book_chart_content where book_id=:book_id and chart_id>:chart_id order by chart_id  limit 1"
        rows = self.db.query(sql, **emp)
        for row in rows:
            data.append(row.as_dict())
        if data:
            return data[0]
        else:
            return None

    # 查询上一章的sql： select * from book_details where book_id=45563 and sort_id<328922 order by sort_id desc limit 1
    def get_before_cap_id(self, book_id, chart_id):
        data = []
        emp = {
            'book_id': book_id,
            'chart_id': chart_id,
        }
        sql = "select chart_id from book_chart_content where book_id=:book_id and chart_id<:chart_id order by chart_id desc limit 1"
        rows = self.db.query(sql, **emp)
        for row in rows:
            data.append(row.as_dict())
        # print(data[0])
        if data:
            return data[0]
        else:
            return None

    def get_books_page(self, book_cate, pageNo, pageSize):
        data = []
        emp = {
            'book_cate': book_cate,
        }
        sql = "SELECT * from book_info where book_cate=:book_cate limit {},{} ".format((pageNo-1)*pageSize, pageSize)
        rows = self.db.query(sql, **emp)
        for row in rows:
            data.append(row.as_dict())
        # print(data)
        if data:
            return data
        else:
            return None

if __name__ == '__main__':
    books = Books()
    books.get_books_page('xuanhuan', 0, 10)