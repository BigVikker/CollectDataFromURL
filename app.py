import validators
from unidecode import unidecode
from flask import Flask, request, render_template
from newspaper import Article

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not validators.url(url) :
            return render_template('index.html')
        else:
            article = Article(url)
            article.download()
            article.parse()
            stringResult = article.title
            file = open("recordFile.txt", "a")
            print(stringResult)
            try:
                file.write(unidecode(stringResult) + "\n")
                file.close()
            except:
                file.close()
            return render_template('index.html', stringResult=stringResult)
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)