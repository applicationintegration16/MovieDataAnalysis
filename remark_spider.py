import requests
import pandas as pd
import time
import random
from lxml import etree


def get_request(url):
    gap = 3
    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    ]


    header = {
        'User-agent': random.choice(UserAgent_List),
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/subject/24773958/?from=showing',
    }

    session = requests.Session()

    cookie = {
        'cookie': "{%22area_code%22:%22+86%22%2C%22number%22:%2218012850228%22%2C%22code%22:%221548%22}",
    }

    time.sleep(random.randint(5, 15))
    response = requests.get(url, headers=header, cookies=cookie, timeout=gap)
    if response.status_code != 200:
        print(response.status_code)
    return response



def start():
    base_url = 'https://movie.douban.com/subject/24773958/comments'
    start_url = base_url + '?start=0'
    num = 1
    html = get_request(start_url)

    while html.status_code == 200:
        selector = etree.HTML(html.text)
        next_page = selector.xpath("//div[@id='paginator']/a[@class='next']/@href")
        next_page = next_page[0]
        next_url = base_url + next_page

        comment_list = selector.xpath("//div[@class='comment']")
        data_list = []

        for comment in comment_list:
            data_list.append(get_comment_list(comment))

        data = pd.DataFrame(data_list)

        try:
            if num == 1:
                csv_headers = ['用户', '是否看过', '五星评分', '评论时间', '有用数', '评论内容']
                data.to_csv('data.csv', header=csv_headers, index=False, mode='a+', encoding='utf-8')
            else:
                data.to_csv('data.csv', header=False, index=False, mode='a+', encoding='utf-8')
        except UnicodeEncodeError:
            print("ENCODE ERROR....")

        data = []
        html = get_request(next_url)


def get_comment_list(comment):
    comment_list = []
    user = comment.xpath("./h3/span[@class='comment-info']/a/text()")[0]
    watched = comment.xpath("./h3/span[@class='comment-info']/span[1]/text()")[0]
    ratings = comment.xpath("./h3/span[@class='comment-info']/span[2]/@title")

    if len(ratings) > 0:
        ratings = ratings[0]

    comment_time = comment.xpath("./h3/span[@class='comment-info']/span[3]/@title")
    if len(comment_time) > 0:
        comment_time = comment_time[0]
    else:
        comment_time = ratings
        ratings = ''

    votes = comment.xpath("./h3/span[@class='comment-vote']/span/text()")[0]
    content = comment.xpath("./p/span/text()")[0]

    print("-----content")
    print(content)

    comment_list.append(user)
    comment_list.append(watched)
    comment_list.append(ratings)
    comment_list.append(comment_time)
    comment_list.append(votes)
    comment_list.append(content.strip())
    print('COMMENT_LIST---------')
    print(comment_list)
    return comment_list

start()