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
            print(article.publish_date)
            stringResult = article.title
            # mo file recordFileUrl.text de luu link url
            file = open("recordFileUrl.txt", "a")
            file.write(url + "\n")
            file.close()
            # mo file recordFile.text
            file = open("recordFileResult.txt.txt", "a")

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
                file = open("recordFileResult.txt.txt", "a")
                file.write(unidecode(article.title) + "\n")
                file.close()
                file = open("recordFileUrl.txt", "a")
                file.write(article.url + "\n")
                file.close()
            return render_template('multi.html', stringResult=len(listResult))
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
            file = open("recordFileResult.txt.txt", "r")
            dataFromFile = file.readline()
            while dataFromFile:
                readder.append(dataFromFile.strip())
                dataFromFile = file.readline()
            file.close()
            file = open("recordFileUrl.txt", "r")
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
                if count > len(SplitUrlLink) / 2:
                    resultString.append(readder[item])
                    resultStringUrl.append(readderUrl[item])
            return render_template('TrangTimKiem.html', len=len(resultString), stringResult=resultString, stringResultUrl=resultStringUrl)
        return render_template('TrangTimKiem.html')
    else:
        return render_template('TrangTimKiem.html')


if __name__ == '__main__':
    app.run(debug=True)