from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from .api_call import *

class Cash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ticker = db.Column(db.String(8))
    symbol = db.Column(db.String(8))
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    desc = db.Column(db.String(1024), default=None)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    
    def curr_price(self):
        return round(get_price(self.ticker), 4)
    
    def pnl(self):
        return round(self.curr_value() - self.value(), 2)
    
    def price_change(self):
        return round((self.curr_price()-self.price)/self.price*100, 2)
    
    def value(self):
        return round(self.price * self.amount, 2)
    
    def curr_value(self):
        return round(self.amount*self.curr_price(), 2)
    
    def __repr__(self):
        return (f'asset №{self.id}: {self.amount} in {self.name}')

    def get_fields_list(self):
        return 'Currency', 'Amount', 'Buy price', 'Price', 'Buy value', 'Value', 'Buy date', 'Description'
    
    def get_fields(self):
        return [self.name, f'{self.amount} {self.symbol}', f'{self.price} $',
                f'{self.curr_price()} $ ({self.price_change()} %)', f'{self.value()} $',
                f'{self.curr_value()} $ ({self.pnl()} $)', datetime.strftime(self.date, '%Y-%m-%d'), self.desc]
     
class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(64))
    ticker = db.Column(db.String(8))
    symbol = db.Column(db.String(8))
    bank = db.Column(db.String(128))
    value = db.Column(db.Float)
    interest = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    due = db.Column(db.DateTime(timezone=True))
    desc = db.Column(db.String(1024), default=None)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    
    def __repr__(self):
        return (f'asset №{self.id}: {self.value}$ deposit in {self.bank}')
    
    def exp_profit(self):
        return round(self.value * self.interest/100/365*(self.due-self.date).days, 2)

    def get_fields_list(self):
        return 'Bank', 'Currency', 'Init value', 'Interest rate', 'Expect value', 'Buy date', 'Due date', 'Description'
    
    def get_fields(self):
        return [self.bank, self.currency, f'{self.value} {self.symbol}', f'{self.interest} %', 
                f'{self.value + self.exp_profit()} {self.symbol} ({self.exp_profit()} {self.symbol})', 
                datetime.strftime(self.date, '%Y-%m-%d'), datetime.strftime(self.due, '%Y-%m-%d'), self.desc]

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ticker = db.Column(db.String(16))
    share = db.Column(db.Float)
    price = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    desc = db.Column(db.String(1024), default=None)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    
    def __repr__(self):
        return (f'asset №{self.id}: {self.share} stocks of {self.name}')
    
    def curr_price(self):
        return round(get_price(self.ticker), 4)
    def pnl(self):
        return round(self.curr_value() - self.value(), 2)
    def price_change(self):
        return round((self.curr_price()-self.price)/self.price*100, 2)
    def value(self):
        return round(self.price * self.share, 2)
    def curr_value(self):
        return round(self.share*self.curr_price(), 2)
    def get_fields_list(self):
        return ['Name', 'Share', 'Buy price', 'Price', 
                'Buy value', 'Value', 'Buy date', 'Description']
    def get_fields(self):
        resp = [self.name, self.share, f'{self.price} $',
                f'{self.curr_price()} $ ({self.price_change()} %)', f'{self.value()} $',
                f'{self.curr_value()} $ ({self.pnl()} $)', 
                datetime.strftime(self.date, '%Y-%m-%d'), self.desc]
        return resp

class Future(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ticker = db.Column(db.String(8))
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    desc = db.Column(db.String(1024), default=None)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    
    def __repr__(self):
        return (f'asset #{self.id}: {self.amount} of {self.name}')
    
    def curr_price(self):
        return round(get_price(self.ticker), 4)
    
    def pnl(self):
        return round(self.curr_value() - self.value(), 2)
    
    def price_change(self):
        return round((self.curr_price()-self.price)/self.price*100, 4)
    
    def value(self):
        return round(self.price * self.amount, 2)
    
    def curr_value(self):
        return round(self.amount*self.curr_price(), 2)
    
    def __repr__(self):
        return (f'asset №{self.id}: {self.amount} in {self.name}')

    def get_fields_list(self):
        return 'Name', 'Amount', 'Buy price', 'Price', 'Buy value', 'Value', 'Buy date', 'Description'
    
    def get_fields(self):
        return [self.name, f'{self.amount}', f'{self.price} $',
                f'{self.curr_price()} $ ({self.price_change()} %)', f'{self.value()} $',
                f'{self.curr_value()} $ ({self.pnl()} $)', datetime.strftime(self.date, '%Y-%m-%d'), self.desc]


class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ticker = db.Column(db.String(16))
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    desc = db.Column(db.String(1024), default=None)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    
    def __repr__(self):
        return (f'asset №{self.id}: {self.amount} in crypto {self.name}')
    
    def curr_price(self):
        return round(get_crypto_price(self.ticker), 4)
    
    def pnl(self):
        return round(self.curr_value() - self.value(), 2)
    
    def price_change(self):
        return round((self.curr_price()-self.price)/self.price*100, 4)
    
    def value(self):
        return round(self.price * self.amount, 2)
    
    def curr_value(self):
        return round(self.amount*self.curr_price(), 2)
    
    def get_fields_list(self):
        return 'Currency', 'Amount', 'Buy price', 'Price', 'Buy value', 'Value', 'Buy date', 'Description'
    
    def get_fields(self):
        return [self.name, f'{self.amount}', f'{self.price} $',
                f'{self.curr_price()} $ ({self.price_change()} %)', f'{self.value()} $',
                f'{self.curr_value()} $ ({self.pnl()} $)', datetime.strftime(self.date, '%Y-%m-%d'), self.desc]


class Other(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    value = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    desc = db.Column(db.String(1024), default=None)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    
    def __repr__(self):
        return (f'asset №{self.id}: {self.amount} in {self.name}')

    def get_fields_list(self):
        return 'Name', 'Value', 'Description'
    
    def get_fields(self):
        return [self.name, self.value, datetime.strftime(self.date, '%Y-%m-%d'), self.desc]


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    desc = db.Column(db.String(1024), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    private = db.Column(db.Boolean, default=True)

    cashs = db.relationship('Cash')
    deposits = db.relationship('Deposit')
    stocks = db.relationship('Stock')
    futures = db.relationship('Future')
    cryptos = db.relationship('Crypto')
    others = db.relationship('Other')

    def cash_value(self):
        return sum([asset.value() for asset in self.cashs])
    def deposit_value(self):
        return sum([asset.value for asset in self.deposits])
    def stock_value(self):
        return sum([asset.value() for asset in self.stocks])
    def future_value(self):
        return sum([asset.value() for asset in self.futures])
    def crypto_value(self):
        return sum([asset.value() for asset in self.cryptos])
    def other_value(self):
        return sum([asset.value for asset in self.others])

    def cash_curr_value(self):
        return sum([asset.curr_value() for asset in self.cashs])
    def stock_curr_value(self):
        return sum([asset.curr_value() for asset in self.stocks])
    def future_curr_value(self):
        return sum([asset.curr_value() for asset in self.futures])
    def crypto_curr_value(self):
        return sum([asset.curr_value() for asset in self.cryptos])

    def cash_percent(self):
        return round(self.cash_curr_value()/self.total_value(), 2)
    def deposit_percent(self):
        return round(self.deposit_value()/self.total_value(), 2)
    def stock_percent(self):
        return round(self.stock_curr_value()/self.total_value(), 2)
    def future_percent(self):
        return round(self.future_curr_value()/self.total_value(), 2)
    def crypto_percent(self):
        return round(self.crypto_curr_value()/self.total_value(), 2)
    def other_percent(self):
        return round(self.other_value()/self.total_value(), 2)
    
    def assets_value(self):
        return {'cash':self.cash_value(), 'deposit': self.deposit_value(), 'stock': self.stock_value(), 
                'future':self.future_value(), 'cryptoasset': self.crypto_value(), 'other': self.other_value()}
    
    def allocation(self):
        return [self.cash_percent(), self.deposit_percent(), self.stock_percent(),
                self.future_percent(), self.crypto_percent(), self.other_percent()]
    
    def total_value(self):
        ttl_val = round(sum([self.cash_value(), self.deposit_value(), self.stock_value(),
                        self.future_value(), self.crypto_value(), self.other_value()]))
        return ttl_val if ttl_val else 0.000001
    def total_curr_value(self):
        return round(sum([self.cash_curr_value(), self.deposit_value(), self.stock_curr_value(), 
                    self.future_curr_value(), self.crypto_curr_value(), self.other_value()]), 2)
    
    def pnl(self):
        return round(self.total_curr_value()-self.total_value(), 2)
    def pnl_percent(self):
        return round(self.pnl()/self.total_value()*100, 2)
    
    def __repr__(self):
        return (f'portfolio "{self.name}" by "{self.user_id}"')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(64))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    first_name = db.Column(db.String(128), default='')
    last_name = db.Column(db.String(128), default='')
    
    portfolios = db.relationship('Portfolio')
    
    def balance(self):
        return sum([portfolio.value for portfolio in self.portfolios])

    def __repr__(self):
        return (f'user {self.username} with email "{self.email}"')

