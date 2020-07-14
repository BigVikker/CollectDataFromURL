import newspaper
# them thu vien validators de kiem tra gia tri tu web tra ve co phai link url hay khong ?
import validators
# them thu vien unidecode de chuan hoa khi ghi nhan vao file
from unidecode import unidecode
# thu vien flask de ploy san pham tren web
from flask import Flask, request, render_template, request_started
# thu vien newspapper de lay du lieu ve
from newspaper import Article
import re

from datetime import date
import xml.etree.ElementTree as ET

import xml.dom.minidom

def insert_into_data(title,url_link,days):
    item = ET.Element('item')
    item1 = ET.SubElement(item, 'name')
    item2 = ET.SubElement(item, 'url')
    item3 = ET.SubElement(item, 'days')
    item1.text = title
    item2.text = url_link
    item3.text = days

    xml_tree = ET.parse("data.xml")
    findElementAppend = xml_tree.find('items')
    findElementAppend.append(item)

    with open('data.xml', "wb") as f:
        f.write(ET.tostring(xml_tree.getroot()))
        f.close()

    return









app = Flask(__name__)

# thu vien flask se mo local host , route dieu kien huong di
# vi du: local host duoc dinh nghia localhost/ va co methods get va post

@app.route('/', methods=['GET', 'POST'])
def index():
    # neu website tra du lieu co method = "POST" thi thuc hien
    if request.method == 'POST':
        # bien url lay du lieu tu from tro ve
        url = request.form['url']
        # kiem tra bien url co phai link url hay khong
        if not validators.url(url):
            # neu khong phai link url thi render file template co ten index.html\
            return render_template('index.html')
        # neu bien url la link url
        else:
            # cac nhiem vu lien quan su dung den thu vien
            article = Article(url)
            # tai dau bao ve
            try:
                article.download()
            except:
                return render_template('index.html', stringResult="err 404")
            # phan tich
            article.parse()
            stringResult = article.title
            # mo file recordFileUrl.text de luu link url
            if article.publish_date == None:
                insert_into_data(article.title, url, '2000-0-0')
            else:
                days = article.publish_date
                insert_into_data(stringResult, url, str(days)[0:10])
            return render_template('index.html', stringResult=article.title)
    else:
        # neu mothed = "Post" thi render file index.html trong template
        return render_template('index.html')


# them trang web thu them tu cac trang chu
@app.route('/thuTapTuTrang', methods=['GET', 'POST'])
def multi():
    # neu website tra du lieu co method = "POST" thi thuc hien
    if request.method == 'POST':
        # bien url lay du lieu tu from tro ve
        url = request.form['url']
        # kiem tra bien url co phai link url hay khong

        if not validators.url(url):
            # neu khong phai link url thi render file template co ten index.html
            return render_template('multi.html')
        # neu bien url la link url

        else:
            # lay tat ca cac link trong link url
            paper = newspaper.build(url)
            for article in paper.articles:
                article.download()
                article.parse()
                if article.publish_date == None:
                    insert_into_data(article.title, article.url, '2010-01-01')
                else:
                    days = article.publish_date
                    insert_into_data(article.title, article.url, str(days)[0:10])
            return render_template('multi.html', stringResult=len(paper.articles))
    else:
        # neu mothed = "Post" thi render file index.html trong template
        return render_template('multi.html')


@app.route('/TimKiem', methods=['GET','POST'])
def TrangTimKiem():
    if request.method == 'POST':
        url = request.form['url']
        if (url == None):
            return render_template('TrangTimKiem.html')
        else:
            mydoc = xml.dom.minidom.parse("data.xml");
            urls = mydoc.getElementsByTagName('url')
            titles = mydoc.getElementsByTagName('name')
            filter_split = url.split()
            resultString = []
            resultStringUrl = []
            for item in range(0,len(titles)):
                count = 0
                for conditions in filter_split:
                    if unidecode(titles[item].firstChild.data.lower()).find(unidecode(conditions.lower())) != -1:
                        count = count + 1
                    if count/len(filter_split) >= 0.5:
                        resultString.append(titles[item].firstChild.data)
                        resultStringUrl.append(urls[item].firstChild.data)

            return render_template('TrangTimKiem.html', len=len(resultString), stringResult=resultString, stringResultUrl=resultStringUrl)
    else:
        return render_template('TrangTimKiem.html')
@app.route('/Analysis')
def Analysis():
    class Complex:
        def __init__(self, realpart, numberPart):
            self.name = realpart
            self.number = numberPart

    mydoc = xml.dom.minidom.parse("data.xml");
    readderFromFile = mydoc.getElementsByTagName('name')
    list = []
    firstInsertToList = readderFromFile[0].firstChild.data.split()
    for i in firstInsertToList:
        if len(list) == 0:
            obj = Complex(i, 1)
            list.append(obj)
            continue

        for item in range(0, len(list)):
            if list[item].name == i:
                list[item].number += 1
                break
            if item == len(list) - 1:
                obj = Complex(i, 1)
                list.append(obj)

    for i in range(1, len(readderFromFile)):
        obj_splitted = readderFromFile[i].firstChild.data.split()
        for item1 in obj_splitted:
            for item in range(0, len(list)):
                if list[item].name == item1:
                    list[item].number += 1
                    break
                if item == len(list) - 1:
                    obj = Complex(item1, 1)
                    list.append(obj)

    list.sort(key=lambda x: x.number, reverse=True)
    list = list[0:10]

    return render_template('PhanTich.html',stringResult=list)


if __name__ == '__main__':
    app.run(debug=True)