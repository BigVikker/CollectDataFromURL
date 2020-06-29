import newspaper
# them thu vien validators de kiem tra gia tri tu web tra ve co phai link url hay khong ?
import validators
# them thu vien unidecode de chuan hoa khi ghi nhan vao file
from unidecode import unidecode
# thu vien flask de ploy san pham tren web
from flask import Flask, request, render_template
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
            article.download()
            article.parse()
            stringResult = article.title
            # mo file recordFile.text
            file = open("recordFile.txt", "a")

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
            # cac nhiem vu lien quan su dung den thu vien
            paper = newspaper.build(url)
            for article in paper.articles:
                article.download()
                article.parse()
                print(article.title)
                listResult.append(article.title)
                file = open("recordFile.txt", "a")
                file.write(unidecode(article.title) + "\n")
                file.close()
        return render_template('multi.html', stringResult=listResult)
    else:
        # neu mothed = "Post" thi render file index.html trong template
        return render_template('multi.html')


if __name__ == '__main__':
    app.run(debug=True)