from flask import Flask, escape, request, render_template
import random
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/lotto')
def lotto():
    numbers = random.sample(range(1,46),6)
    print(numbers)
    return render_template('lotto.html', numbers=numbers)

@app.route('/lunch')
def lunch():
    lunch_menus = [
        '오징어주꾸미볶음', 
        '나주곰탕', 
        '순두부짬뽕밥',
        '소시지투움바파스타',
        '만두라면',
        '버섯닭개장'
    ]
    lunch_menu = random.choice(lunch_menus)
    print(lunch_menu)
    return render_template('lunch.html', lunch_menu=lunch_menu)

@app.route('/op_gg')
def op_gg():
    return render_template('op_gg.html')

@app.route('/search')
def search():
    op_gg_url = "https://www.op.gg/summoner/userName="
    summoner = request.args.get('summoner')
    url = op_gg_url + summoner

    res = requests.get(url).text

    soup = BeautifulSoup(res, 'html.parser')
    tier = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank')
    user_tier = tier.text.strip()

    return render_template('search.html', user_tier=user_tier, summoner=summoner)

@app.route('/nono')
def nono():
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        products = list(reader)
    return render_template('nono.html', products=products)
# 원래 'nono.html'은 진짜 html이 아니야. 근데 render_template을 통해서 진짜 html이 되는거야. 렌더링하는 거라구~

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create')
def create():
    product = request.args.get('product')
    category = request.args.get('category')
    replace = request.args.get('replace')

    with open('data.csv', 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        #['해피해킹', '키보드', '한성']
        product_info = [product, category, replace]
        writer.writerow(product_info)
    return render_template('create.html')

@app.route('/nono_card')
def nono_card():
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        products = list(reader)
    return render_template('nono_card.html', products=products)

if __name__ == "__main__":
    app.run(debug=True)