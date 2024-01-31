
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))

# Create the database tables
db.create_all()

# Define the home page
@app.route('/')
def home():
    expenses = Expense.query.all()
    return render_template('home.html', expenses=expenses)

# Define the route to add a new expense
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        expense = Expense(name=request.form['name'], amount=request.form['amount'], category=request.form['category'])
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

# Define the route to edit an expense
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense.name = request.form['name']
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', expense=expense)

# Define the route to delete an expense
@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
