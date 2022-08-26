from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.user import Product
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 



@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/signup')
    data = {
        'id': session['user_id']
    }
    return render_template('index.html', user = User.get_by_id(data))


@app.route('/signup')
def signup():
    return render_template('signup.html')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/signup')
    data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        'address': request.form['address'],
        'zipcode': request.form['zipcode'],
        'city': request.form['city'],
        'state': request.form['state'],
        'country': request.form['country'],
        'phone': request.form['phone'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/')


@app.route('/validate', methods=['POST'])
def validate():
    data = { 'email' : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect ('/login')
    elif not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/logoutAdmin')
def logoutAdmin():
    session.clear()
    return redirect('/admin')


@app.route('/admin')
def admin():
    if 'user_id' in session:
        session.clear()
    return render_template('admin.html')


@app.route('/validateAdmin', methods=['POST'])
def validateAdmin():
    data = { 'email' : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect ('/admin')
    elif not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/admin')
    session['user_id'] = user_in_db.id
    if user_in_db.admin == True:
        return redirect('/admin')
    else:
        flash("You are not an admin!", 'admin')
        return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/create', methods=['POST'])
def create():
    data = {
        'name': request.form['name'],
        'price': request.form['price'],
        'description': request.form['description'],
        'image': request.form['image'],
        'stock': request.form['stock'],
        'category_id': request.form['category_id']
    }
    Product.save(data)
    return redirect('/dashboard')
