# coding=utf-8

import os
import urllib2
import urllib
from bs4 import BeautifulSoup
import chardet
import pickle
import jieba
import sys
import re

user_dict = ['假的', '消息不实', '不实', '真的吗', '不属实', '别再传', '勿信']
for word in user_dict:
    jieba.add_word(word)

BAIDU = 'http://www.baidu.com'
news_filepath = 'fake_news.txt'
stopwords_filepath = 'stop_words.txt'
news_list = []
stop_words = set([])


def load_news():
    news_list = []
    with open(news_filepath) as file:
        for news in file:
            news_list.append(news.decode('utf-8').strip())
    return news_list


news_list = load_news()


def load_stop_words():
    stop_words = []
    with open(stopwords_filepath) as file:
        for word in file:
            stop_words.append(word.decode('utf-8').strip())
    return set(stop_words)


stop_words = load_stop_words()


def query_baidu(query_str):
    results_title = []
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
    headers = {"User-Agent": user_agent}

    # 第一页结果
    request = urllib2.Request(BAIDU + '/s?wd=' + urllib.quote(query_str.encode('gbk')),
                              headers=headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response.read(), "lxml")
    results_title.extend(get_query_results(soup))

    # 第二页结果
    next_page = soup.find(id='page').find_all('a')[-1].get('href')
    request = urllib2.Request(BAIDU + next_page, headers=headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response.read(), "lxml")
    results_title.extend(get_query_results(soup))
    return results_title


def get_query_results(soup):
    results = soup.find_all(attrs={'class': 'result c-container '})
    results_title = []
    for result in results:
        link = result.find('a')
        if link.text.find('...') != -1:
            request = urllib2.Request(link.get('href'))
            html = ''
            try:
                response = urllib2.urlopen(request, timeout=40)
                html = response.read()
                soup = BeautifulSoup(html, "lxml")
                results_title.append(soup.title.text)
            except Exception, e:
                print '******get exception when get url: ' + request.get_full_url()
                print  chardet.detect(html)
                print  Exception, ":", e
                results_title.append(link.text)

        else:
            results_title.append(link.text)
            print link.text
    return results_title


def catch_and_save():
    new_results_map = {}
    for news in news_list:
        print '--get results for: ' + news
        query_results = query_baidu(news)
        new_results_map[news] = query_results
    mydb = open('new_results_map', 'w')
    pickle.dump(new_results_map, mydb)


def test():
    import pickle
    import re
    from collections import defaultdict
    word_count = defaultdict(int)
    r = re.compile("-|_|—.*")
    mydb = open('new_results_map', 'r')
    new_results_map = pickle.load(mydb)
    for news in news_list:
        news_word = set(jieba.cut(news))
        for query_result in new_results_map[news]:
            title = r.split(query_result.strip())[0]
            words = jieba.cut(title)
            for word in words:
                if word not in news_word and word not in stop_words and word != u' ':
                    word_count[word] += 1
                    if word == u'勿':
                        print title
                else:
                    pass
    word_count = sorted(word_count.iteritems(), key=lambda x: x[1], reverse=True)
    mydb = open('word_count', 'w')
    pickle.dump(word_count, mydb)
    file = open('word_count.txt', 'w')
    for word, count in word_count:
        # print word, count
        file.write((word + ' ' + str(count) + '\n').encode('utf-8'))
    file.close()


if __name__ == '__main__':
    import time

    print 'start: -----------------------'
    start = time.time()
    test()
    print 'end:-----------------', time.time() - start
