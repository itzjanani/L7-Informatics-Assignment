from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import extract
from utils.email_alert import send_budget_alert_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_1aHnCSBph0EL@ep-purple-lake-a5mdfrwl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------- MODELS ---------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
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
    category = db.Column(db.String(50), nullable=False)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    month = db.Column(db.String(10), nullable=False)  # e.g., '2025-04'
    amount = db.Column(db.Float, nullable=False)
    remaining = db.Column(db.Float, nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class GroupExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200))
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------- ROUTES ---------------------

@app.route('/')
def index():
    user_id = request.args.get('user_id')

    if not user_id:
        return render_template(
            'index.html',
            users=[],
            categories=[],
            expenses=[],
            groups=[],
            members=[],
            gexpenses=[],
            budgets=[]
        )

    return render_template(
        'index.html',
        users=User.query.all(),
        categories=Category.query.all(),
        expenses=Expense.query.filter_by(user_id=user_id).all(),
        groups=Group.query.filter_by(user_id=user_id).all(),
        members=GroupMember.query.filter_by(user_id=user_id).all(),
        budgets=Budget.query.filter_by(user_id=user_id).all()
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'User already exists'}), 400

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 401

        if user.password != password:
            return jsonify({'message': 'Invalid password'}), 401

        return jsonify({'message': 'Login successful', 'id': user.id, 'name': user.name})
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'})


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

    try:
        expense_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        expense_date = datetime.utcnow().date()
        
    expense = Expense(
        amount=data['amount'],
        description=data.get('description'),
        date=expense_date,
        user_id=data['user_id'],
        category=data['category']
    )
    db.session.add(expense)
    
    expense_month = expense_date.strftime('%Y-%m')

    budget = Budget.query.filter_by(
        user_id=data['user_id'],
        category=data['category'],
        month=expense_month
    ).first()

    if budget:
        budget.remaining -= float(data['amount'])
        print(budget)
        if budget.amount * 0.1 >= budget.remaining:
            user = User.query.get(data['user_id'])  
            if user:
                send_budget_alert_email(user.email, data['category'], budget.remaining)
        
    db.session.commit()
    return jsonify({'message': 'Expense added'})

@app.route('/budget', methods=['POST'])
def set_budget():
    data = request.json
    user_id = data['user_id']
    category = data['category']
    month = data['month']
    amount = float(data['amount'])
    
    existing_budget = Budget.query.filter_by(
        user_id=user_id,
        category=category,
        month=month
    ).first()


    if existing_budget:
        # Update existing budget
        existing_budget.amount += amount
        existing_budget.remaining += amount
        message = 'Budget updated successfully'
    else:
        # Create new budget entry
        budget = Budget(
            user_id=user_id,
            category=category,
            month=month,
            amount=amount,
            remaining=amount
        )
        db.session.add(budget)
        message = 'Budget set successfully'

    db.session.commit()
    return jsonify({'message': message}), 201


@app.route('/group', methods=['POST'])
def create_group():
    data = request.json
    group = Group(name=data['name'],user_id=data['user_id'])
    db.session.add(group)
    db.session.commit()
    return jsonify({'message': 'Group created'})

@app.route('/group/member', methods=['POST'])
def add_group_member():
    data = request.json
    existing = GroupMember.query.filter_by(
        group_id=data['group_id'], 
        user_id=data['user_id']
    ).first()
    
    if existing:
        return jsonify({'error': 'User is already a member of this group'}), 400

    member = GroupMember(group_id=data['group_id'], user_id=data['user_id'])
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Member added to group'})

@app.route('/group/expense', methods=['POST'])
def add_group_expense():
    data = request.json
    group = Group.query.filter_by(id=data['group_id']).first()

    if not group:
        return jsonify({'error': 'Group or Category not found'}), 400

    members = GroupMember.query.filter_by(group_id=group.id).all()
    print(members)
    if not members:
        return jsonify({'error': 'No members in group'}), 400
    
    try:
        expense_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        expense_date = datetime.utcnow().date()

    per_person_amount = float(data['amount']) / len(members)
    print(per_person_amount)
    for member in members:
        expense = Expense(
            user_id=member.user_id,
            category= data['category_name'],
            amount=per_person_amount,
            description="GROUP Exp : "+ group.name + "->" + data['description'],
            date=expense_date
        )
        db.session.add(expense)

    group_expense = GroupExpense(
        group_id=group.id,
        amount=data['amount'],
        description=data.get('description'),
        category=data['category_name'],
        date=expense_date,
        user_id=data['user_id']
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

@app.route('/api/expenses/monthly', methods=['GET'])
def get_monthly_expenses():
    user_id = request.args.get('user_id', type=int)
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    if not user_id or not month or not year:
        return jsonify({'error': 'Missing parameters'}), 400

    expenses = Expense.query.filter(
        Expense.user_id == user_id,
        extract('month', Expense.date) == month,
        extract('year', Expense.date) == year
    ).all()

    data = {}
    total = 0

    for exp in expenses:
        data[exp.category] = data.get(exp.category, 0) + exp.amount
        total += exp.amount

    result = {
        'categories': [{'category': cat, 'amount': amt} for cat, amt in data.items()],
        'total': total
    }
    return jsonify(result)

# --------------------- MAIN ---------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
