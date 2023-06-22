from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .validator import *
from .models import *
from . import db
from datetime import datetime
from .api_call import *
import os
import matplotlib.pyplot as plt


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user) 

def page_not_found(e):
    flash(f'This page doesn`t exist', category="error")
    return render_template('404.html', user=current_user), 404


@views.route('/portfolder')
@login_required
def portfolder():
    return render_template("portfolder.html", user=current_user)

@views.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        desc = data.get('desc')
        private = data.get('private')

        name_check = valid_name(name)
        desc_check = valid_desc(desc)

        if any([name == portfolio.name for portfolio in current_user.portfolios]):
            flash(f'You already have portfolio "{name}"', category="error")
        elif not name_check[0]:
            flash(name_check[1], category="error")
        elif not desc_check[0]:
            flash(desc_check[1], category="error")
        else:
            new_portfolio = Portfolio(name=name, desc=desc, user_id=current_user.id, private=(private=='1'))
            db.session.add(new_portfolio)
            db.session.commit()
            flash(f'Portfolio "{name}" created, time to add your investments', category="success")
            return redirect(url_for('views.portfolder'))

    return render_template("create.html", user=current_user)

@views.route('/portfolio/<id>')
@login_required
def portfolio(id):
    portfolio = Portfolio.query.get(id)
    if not portfolio:
        flash('This portfolio doesn`t exist', category="error")
        return redirect(url_for("views.home"))
    if portfolio.total_curr_value():
        
        labels = 'Cash', 'Deposits', 'Stocks', 'Futures', 'Crypto', 'Other'
        sizes = portfolio.allocation()
        colors=['#61b04c', 'rosybrown', '#b0704c', '#4d5380', '#4bad91',  'gray']
        valid_labels = []
        valid_sizes = []
        for i, size in enumerate(sizes):
            if size != 0:
                valid_labels.append(labels[i])
                valid_sizes.append(size)
        fig, ax = plt.subplots()
        ax.pie(valid_sizes, labels=valid_labels, autopct='%1.1f%%', colors=colors)
        img_path = os.path.join(os.path.dirname(__file__), f"static/images/portfolio_{portfolio.id}.png")
        fig.savefig(img_path)

        recomends = get_ai_recommendation(current_user, portfolio)
        print(recomends)
    return render_template("portfolio.html", user=current_user, portfolio=portfolio, 
                           allocation = bool(portfolio.total_curr_value()), recomends=recomends)


@views.route('/profile/<login>')
@login_required
def profile(login):
    user = User.query.filter_by(username=login).first()
    if not user:
        flash(f'This user doesn`t exist', category="error")
        return redirect(url_for("views.home"))
    return render_template("profile.html", user=current_user)

@views.route('/settings')
@login_required
def settings():
    return render_template("settings.html", user=current_user)


@views.route('/portfolio/<id>/delete')
@login_required 
def delete_portfolio(id):
    portfolio = Portfolio.query.get(id)
    if portfolio:
        if portfolio.user_id == current_user.id:
            db.session.delete(portfolio)
            db.session.commit()
            flash(f'Portfolio "{portfolio.name}" and all assets from it was deleted', category="success")
        else:
            flash(f'You have no permission to modify this portfolio', category="error")
    else:
        flash(f'This portfolio doesn`t exist', category="error")

    return redirect(url_for("views.portfolder"))

@views.route('/portfolio/<id>/add', methods=['GET', 'POST'])
@login_required 
def add_asset(id):
    portfolio = Portfolio.query.get(id)
    if not portfolio:
        flash(f'This portfolio doesn`t exist', category="error")
        return redirect(url_for('views.portfolio', id=id))

    if portfolio.user_id != current_user.id:
        flash(f'You have no permission to modify this portfolio', category="error")
        return redirect(url_for('views.portfolio', id=id))
    if request.method == 'POST':
        data = request.form
        print(data)
        asset_category = data.get('asset-category')
        if asset_category == "cash":
            add_cash(data, portfolio)
        elif asset_category == "deposit":
            add_deposit(data, portfolio)
        elif asset_category == "stocks":
            add_stock(data, portfolio)
        elif asset_category == "futures":
            add_future(data, portfolio)
        elif asset_category == "crypto":
            add_crypto(data, portfolio)
        elif asset_category == "other":
            add_other(data, portfolio)
        
        return redirect(url_for('views.portfolio', id=id))

    today = datetime.today().strftime('%Y-%m-%d')
    currencies = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/currencies.json")))
    stocks = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/stocks.json")))
    futures = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/futures.json")))
    cryptocurrencies = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/crypto.json")))
    print(len(currencies))
    print(len(stocks))
    print(len(futures))
    print(len(cryptocurrencies))

    return render_template("add.html", 
                            user=current_user, 
                            portfolio=portfolio, 
                            today=today, 
                            currencies=currencies, 
                            stocks=stocks, 
                            futures = futures,
                            cryptocurrencies = cryptocurrencies)

@views.route('/portfolio/<portfolio_id>/<asset>/<id>/delete')
@login_required 
def delete_asset(portfolio_id, asset, id):
    asset_dict = {'cash':Cash,
                  'deposit':Deposit}
    asset = asset_dict.get(asset).query.get(id)
    portfolio = Portfolio.query.get(asset.portfolio_id)

    if asset and portfolio:
        if portfolio.user_id == current_user.id:
            db.session.delete(asset)
            db.session.commit()
            flash(f'"{str(asset)}" was deleted', category="success")
        else:
            flash(f'You have no permission to modify this asset', category="error")
    else:
        flash(f'This asset doesn`t exist', category="error")

    return redirect(url_for('views.portfolio', id=portfolio_id))

def add_cash(data, portfolio):
    currency = data.get('currency')
    amount = float(data.get('amount'))
    price = data.get('price')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    desc = data.get('desc')
    currencies = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/currencies.json")))
    for curr in currencies:
        if currency.replace(' ', '').split('-')[0] == curr.get('ticker')[:3]:
            ticker = curr.get('ticker')
            symbol = curr.get('symbol')
            name = curr.get('name')
            if not price: price = get_price(ticker, date)
            new_asset = Cash(name=name, ticker=ticker,
                             symbol=symbol, amount=amount, price=float(price),
                             date=date, desc=desc,
                             portfolio_id=portfolio.id)
            db.session.add(new_asset)
            db.session.commit()
            flash(f'Successfully added new asset in category "Cash" to "{portfolio.name}"!', category="success")
            return 1
    flash('That currency doesn`t supported"!', category="error")

def add_deposit(data, portfolio):
    currency = data.get('currency')
    bank = data.get('bank')
    value = float(data.get('value'))
    interest = float(data.get('percent'))
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    due = datetime.strptime(data.get('due'), '%Y-%m-%d')
    desc = data.get('desc')

    currencies = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/currencies.json")))
    for curr in currencies:
        if currency.replace(' ', '').split('-')[0] == curr.get('ticker')[:3]:
            ticker = curr.get('ticker')
            symbol = curr.get('symbol')
            name = curr.get('name')
            new_asset = Deposit(currency=name, ticker=ticker,
                             symbol=symbol, bank=bank, value=value, interest=interest,
                             date=date, due=due, desc=desc, portfolio_id=portfolio.id)
            db.session.add(new_asset)
            db.session.commit()
            flash(f'Successfully added new asset in category "Deposit" to "{portfolio.name}"!', category="success")
            return 1
    flash('That currency doesn`t supported"!', category="error")

def add_stock(data, portfolio):
    stock = data.get('stock')
    share = float(data.get('share'))
    price = data.get('price')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    desc = data.get('desc')
    stocks = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/stocks.json")))
    for stck in stocks:
        if stock.replace(' ', '').split('-')[0] == stck.get('ticker'):
            ticker = stck.get('ticker')
            name = stck.get('name')
            if not price: price = get_price(ticker, date)
            new_asset = Stock(name=name, ticker=ticker,
                             share=share, price=float(price),
                             date=date, desc=desc, portfolio_id=portfolio.id)
            db.session.add(new_asset)
            db.session.commit()
            flash(f'Successfully added new asset in category "Stocks" to "{portfolio.name}"!', category="success")
            return 1
    flash('That stock doesn`t supported"!', category="error")


def add_future(data, portfolio):
    future = data.get('future')
    amount = float(data.get('amount'))
    price = data.get('price')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    desc = data.get('desc')
    futures = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/futures.json")))
    for ftr in futures:
        if future.replace(' ', '').split('-')[0] == ftr.get('ticker').split('=')[0]:
            print("allgood")
            ticker = ftr.get('ticker')
            name = ftr.get('name')
            if not price: price = get_price(ticker, date)
            new_asset = Future(name=name, ticker=ticker,
                             amount=amount, price=float(price),
                             date=date, desc=desc, portfolio_id=portfolio.id)
            db.session.add(new_asset)
            db.session.commit()
            flash(f'Successfully added new asset in category "Cash" to "{portfolio.name}"!', category="success")
    flash('That future doesn`t supported"!', category="error")


def add_crypto(data, portfolio):
    name = data.get('cryptocurrency')
    amount = float(data.get('amount'))
    price = data.get('price')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    desc = data.get('desc')
    crypto = json.load(open(os.path.join(os.path.dirname(__file__), "static/lists/crypto.json")))
    for curr in crypto:
        if name.replace(' ', '').split('-')[0] == curr.get('ticker').split('-')[0]:
            print("allgood")
            ticker = curr.get('ticker')
            name = curr.get('name')
            if not price: price = get_price(ticker, date)
            new_asset = Crypto(name=name, ticker=ticker,
                             amount=amount, price=float(price),
                             date=date, desc=desc, portfolio_id=portfolio.id)
            db.session.add(new_asset)
            db.session.commit()
            flash(f'Successfully added new asset in category "Crypto assets" to "{portfolio.name}"!', category="success")
    flash('That cryptocurrency doesn`t supported"!', category="error")

def add_other(data, portfolio):
    name = data.get('name')
    value = float(data.get('value'))
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    desc = data.get('desc')
    print("allgood")
    new_asset = Other(name=name, value=value, 
                    date=date, desc=desc, portfolio_id=portfolio.id)
    db.session.add(new_asset)
    db.session.commit()
    flash(f'Successfully added new asset in category "Others" to "{portfolio.name}"!', category="success")
