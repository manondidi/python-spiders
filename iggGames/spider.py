import requests
from bs4 import BeautifulSoup
import json
import pymysql

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; nxt-al10 Build/LYZ28N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 sinablog-android/5.3.2 (Android 5.1.1; zh_CN; huawei nxt-al10/nxt-al10)",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
}

conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='spider',
    charset='utf8mb4'
)


def start():
    next_page(1)
    conn.close()


def next_page(page):
    r = requests.get(url='https://igg-games.com/page/' + str(page), data=None, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find_all("article")
    items = list(map(convert_item, articles))
    save_data(items)
    if not check_end(soup, page):
        next_page(page + 1)


def save_data(items):
    jsonStr = json.dumps(items, default=lambda obj: obj.__dict__)
    print(jsonStr)
    cursor = conn.cursor()  # 获取游标
    sql = "INSERT INTO T_IGGGAMES_COM (title,intro,image_url,publish_time) VALUES (%s,%s,%s,%s)"  # sql语句
    for item in items:
        cursor.execute(sql, (
            item.title, item.desc, item.img, item.time))

    conn.commit()  # 提交事务



def check_end(soup, page):
    """是否结束"""
    return soup.find('a', class_="next page-numbers") is None or page > 5


def convert_item(article):
    img = article.find_all('img', class_='attachment-post-thumbnail size-post-thumbnail wp-post-image')[1]['src']
    title = article.find('h2', class_='uk-margin-large-top uk-margin-remove-bottom uk-article-title').a.text
    time = article.find('time')['datetime']
    desc = article.find('div', class_='uk-margin-medium-top').p.text
    return ArticleItem(img, title, time, desc)


class ArticleItem:
    def __init__(self, img, title, time, desc):
        self.img = img
        self.title = title
        self.time = time
        self.desc = desc

    def __str__(self):
        return '\n' + self.img + '\n' + self.title + '\n' + self.time + '\n' + self.desc


if __name__ == '__main__':
    start()
