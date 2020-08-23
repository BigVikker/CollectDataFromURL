import newspaper
# them thu vien validators de kiem tra gia tri tu web tra ve co phai link url hay khong ?
import validators
# them thu vien unidecode de chuan hoa khi ghi nhan vao file
from unidecode import unidecode
# thu vien flask de ploy san pham tren web
from flask import Flask, request, render_template, request_started
# thu vien newspapper de lay du lieu ve
from newspaper import Article

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
            # mo file recordFile.text
            file = open("articleData/recordFile.txt", "a")

            try:
                # luu lai du lieu da thu thap bang ghi vao file
                # unidecode de ma hoa sang bang chu cai tieng anh
                file.write(unidecode(stringResult) + "\n")
                # dong file
                file.close()
            except:
                # neu co trong qua trinh ghi file loi thi dong file
                file.close()
            # tro ve file chay file index.html co vien tra ve stringResult trong file template
            return render_template('index.html', stringResult=stringResult)
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
        listResult = []

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
                listResult.append(article.title)
                file = open("articleData/recordFileResult.txt.txt", "a")
                file.write(unidecode(article.title) + "\n")
                file.close()
                file = open("articleData/recordFileUrl.txt", "a")
                file.write(article.url + "\n")
                file.close()
            return render_template('multi.html', stringResult=listResult)
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
            readder = []
            readderUrl = []
            file = open("articleData/recordFileResult.txt.txt", "r")
            dataFromFile = file.readline()
            while dataFromFile:
                readder.append(dataFromFile.strip())
                dataFromFile = file.readline()

            file.close()
            file = open("articleData/recordFileUrl.txt", "r")
            dataFromFileUrl = file.readline()
            while dataFromFileUrl:
                readderUrl.append(dataFromFileUrl.strip())
                dataFromFileUrl = file.readline()
            file.close()
            SplitUrlLink = url.split()
            resultString = []
            resultStringUrl = []
            for item in range(0,len(readder)):
                count = 0
                for conditions in SplitUrlLink:
                    if readder[item].lower().find(unidecode(conditions.lower())) != -1:
                        count = count + 1
                if count >= len(SplitUrlLink) / 2:
                    resultString.append(readder[item])
                    resultStringUrl.append(readderUrl[item])
            return render_template('TrangTimKiem.html', len=len(resultString), stringResult=resultString, stringResultUrl=resultStringUrl)
        return render_template('TrangTimKiem.html')
    else:
        return render_template('TrangTimKiem.html')
@app.route('/Analysis')
def Analysis():
    class Complex:
        def __init__(self, realpart, numberPart):
            self.name = realpart
            self.number = numberPart

    readderFromFile = []
    file = open("articleData/recordFileResult.txt.txt", "r")
    dataFromFile = file.readline()
    while dataFromFile:
        readderFromFile.append(dataFromFile.strip().lower())
        dataFromFile = file.readline()
    file.close()

    list = []
    firstInsertToList = readderFromFile[0].split()
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
        obj_splitted = readderFromFile[i].split()
        for item1 in obj_splitted:
            for item in range(0, len(list)):
                if list[item].name == item1:
                    list[item].number += 1
                    break
                if item == len(list) - 1:
                    obj = Complex(item1, 1)
                    list.append(obj)

    list.sort(key=lambda x: x.number, reverse=True)
    list = list[:10]

    return render_template('PhanTich.html',stringResult=list)



if __name__ == '__main__':
    app.run(debug=True)


