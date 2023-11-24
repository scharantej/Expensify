 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Expense %r>' % self.id

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        expense = Expense(amount=amount, category=category, date=date)
        db.session.add(expense)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_expense.html')

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        expense.amount = amount
        expense.category = category
        expense.date = date
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit_expense.html', expense=expense)

@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/reports')
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run()
