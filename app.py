from flask import Flask
from flask_mysqldb import MySQL


mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def login():

    return render_template('index.html', mesage = mesage)

@app.route('/login', methods =['GET', 'POST'])
def login():

    return render_template('login.html', mesage = mesage)

@app.route('/register', methods =['GET', 'POST'])
def login():

    return render_template('register.html', mesage = mesage)

@app.route('/profile', methods =['GET', 'POST'])
def login():

    return render_template('profile.html', mesage = mesage)

@app.route('/main', methods =['GET', 'POST'])
def login():

    return render_template('main.html', mesage = mesage)

@app.route('/portfolio', methods =['GET', 'POST'])
def login():

    return render_template('view_portfolio.html', mesage = mesage)

@app.route('/investment', methods =['GET', 'POST'])
def login():

    return render_template('view_investment.html', mesage = mesage)

@app.route('/edit', methods =['GET', 'POST'])
def login():

    return render_template('edit_investment.html', mesage = mesage)

@app.route('/create', methods =['GET', 'POST'])
def login():

    return render_template('create_investment.html', mesage = mesage)