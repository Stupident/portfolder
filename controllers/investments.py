from flask import Blueprint, render_template, request

investments_bp = Blueprint('investments', __name__)

@investments_bp.route('/create_investment', methods=['GET', 'POST'])
def create_investment():
    if request.method == 'POST':
        # Handle investment creation form submission
        investment_name = request.form.get('name')
        investment_type = request.form.get('type')
        # Perform investment creation logic
        return render_template('view_investment.html', investment_name=investment_name)
    # Render the investment creation form template for GET request
    return render_template('create_investment.html')

@investments_bp.route('/edit_investment', methods=['GET', 'POST'])
def edit_investment():
    if request.method == 'POST':
        # Handle investment edit form submission
        investment_id = request.form.get('id')
        # Fetch investment details from database based on investment_id
        # Perform investment edit logic
        return render_template('view_investment.html', investment_name='Updated Investment')
    # Render the investment edit form template for GET request
    return render_template('edit_investment.html')

@investments_bp.route('/delete_investment', methods=['POST'])
def delete_investment():
    investment_id = request.form.get('id')
    # Perform investment deletion logic
    return 'Investment deleted successfully!'
