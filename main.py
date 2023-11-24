 
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'secret-key'

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Expense %r>' % self.name

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
    expenses = Expense.query.all()
    categories = Category.query.all()
    return render_template('index.html', expenses=expenses, categories=categories)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        amount = request.form['amount']
        date = request.form['date']

        expense = Expense(name=name, category=category, amount=amount, date=date)
        db.session.add(expense)
        db.session.commit()

        flash('Expense added successfully!')
        return redirect(url_for('index'))

    return render_template('add_expense.html')

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'POST':
        expense.name = request.form['name']
        expense.category = request.form['category']
        expense.amount = request.form['amount']
        expense.date = request.form['date']

        db.session.commit()

        flash('Expense updated successfully!')
        return redirect(url_for('index'))

    return render_template('edit_expense.html', expense=expense)

@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    db.session.delete(expense)
    db.session.commit()

    flash('Expense deleted successfully!')
    return redirect(url_for('index'))

@app.route('/get_expenses')
def get_expenses():
    expenses = Expense.query.all()
    return jsonify(expenses=[expense.to_dict() for expense in expenses])

@app.route('/get_categories')
def get_categories():
    categories = Category.query.all()
    return jsonify(categories=[category.to_dict() for category in categories])

@app.route('/get_spending_over_time')
def get_spending_over_time():
    expenses = Expense.query.all()
    spending_over_time = {}
    for expense in expenses:
        if expense.date.month not in spending_over_time:
            spending_over_time[expense.date.month] = 0
        spending_over_time[expense.date.month] += expense.amount
    return jsonify(spending_over_time=spending_over_time)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
