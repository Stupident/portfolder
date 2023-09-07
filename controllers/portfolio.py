from flask import Blueprint, render_template

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/profile')
def profile():
    # Fetch user profile details from the database
    username = 'Eugene'  # Fetch from database
    investments = ['Investment 1', 'Investment 2']  # Fetch from database
    return render_template('profile.html', username=username, investments=investments)

@portfolio_bp.route('/view_portfolio')
def view_portfolio():
    # Fetch user's investment portfolio details from the database
    investments = ['Investment 1', 'Investment 2']  # Fetch from database
    return render_template('view_portfolio.html', investments=investments)

@portfolio_bp.route('/view_investment/<investment_id>')
def view_investment(investment_id):
    # Fetch investment details from the database based on investment_id
    investment_name = 'Investment 1'  # Fetch from database
    return render_template('view_investment.html', investment_name=investment_name)
