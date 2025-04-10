from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------- MODELS ---------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    month = db.Column(db.String(10), nullable=False)  # e.g., '2025-04'
    amount = db.Column(db.Float, nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class GroupExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------- ROUTES ---------------------

@app.route('/')
def index():
    return render_template(
        'index.html',
        users=User.query.all(),
        categories=Category.query.all(),
        expenses=Expense.query.all(),
        groups=Group.query.all(),
        members=GroupMember.query.all(),
        gexpenses=GroupExpense.query.all(),
        budgets=Budget.query.all()
    )

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/category', methods=['POST'])
def create_category():
    data = request.json
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created'})

@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.json
    expense = Expense(
        amount=data['amount'],
        description=data.get('description'),
        date=data.get('date', datetime.utcnow()),
        user_id=data['user_id'],
        category_id=data['category_id']
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense added'})

@app.route('/budget', methods=['POST'])
def set_budget():
    data = request.json
    budget = Budget(
        user_id=data['user_id'],
        category_id=data['category_id'],
        month=data['month'],
        amount=data['amount']
    )
    db.session.add(budget)
    db.session.commit()
    return jsonify({'message': 'Budget set successfully'})

@app.route('/group', methods=['POST'])
def create_group():
    data = request.json
    group = Group(name=data['name'])
    db.session.add(group)
    db.session.commit()
    return jsonify({'message': 'Group created'})

@app.route('/group/member', methods=['POST'])
def add_group_member():
    data = request.json
    member = GroupMember(group_id=data['group_id'], user_id=data['user_id'])
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Member added to group'})

@app.route('/group/expense', methods=['POST'])
def add_group_expense():
    data = request.json
    group = Group.query.filter_by(name=data['group_name']).first()
    category = Category.query.filter_by(name=data['category_name']).first()

    if not group or not category:
        return jsonify({'error': 'Group or Category not found'}), 400

    members = GroupMember.query.filter_by(group_id=group.id).all()
    if not members:
        return jsonify({'error': 'No members in group'}), 400

    per_person_amount = float(data['amount']) / len(members)
    for member in members:
        expense = Expense(
            user_id=member.user_id,
            category_id=category.id,
            amount=per_person_amount,
            description=data.get('description'),
            date=data.get('date', datetime.utcnow())
        )
        db.session.add(expense)

    group_expense = GroupExpense(
        group_id=group.id,
        amount=data['amount'],
        description=data.get('description'),
        category_id=category.id,
        date=data.get('date', datetime.utcnow())
    )
    db.session.add(group_expense)
    db.session.commit()
    return jsonify({'message': 'Group expense added and split among members'})

@app.route('/resolve-ids', methods=['POST'])
def resolve_ids():
    data = request.json
    user = User.query.filter_by(name=data.get('user_name')).first()
    category = Category.query.filter_by(name=data.get('category_name')).first()
    group = Group.query.filter_by(name=data.get('group_name')).first()
    return jsonify({
        'user_id': user.id if user else None,
        'category_id': category.id if category else None,
        'group_id': group.id if group else None
    })

# --------------------- MAIN ---------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
