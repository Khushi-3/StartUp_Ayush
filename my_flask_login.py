from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'mongodb://localhost/your_database_name'
}

db = MongoEngine(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model for MongoDB
class User(UserMixin, db.Document):
    first_name = db.StringField()
    last_name = db.StringField()
    email = db.EmailField(unique=True)
    gender = db.StringField()
    country = db.StringField()
    state = db.StringField()
    username = db.StringField(unique=True)
    password = db.StringField()

# Load user by ID
@login_manager.user_loader
def load_user(user_id):    return User.objects(username=user_id).first()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']
        country = request.form['country']
        state = request.form['state']
        username = request.form['username']
        password = request.form['password']
        password_hashed = generate_password_hash(password, method='sha256')

        if User.objects(username=username):
            flash('Username already exists. Please choose another one.', 'error')
        elif User.objects(email=email):
            flash('Email already exists. Please use another email.', 'error')
        else:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                gender=gender,
                country=country,
                state=state,
                username=username,
                password=password_hashed
            )
            user.save()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return f'Welcome, {current_user.username}! This is your profile page.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
