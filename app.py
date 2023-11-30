from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import render_template, jsonify, redirect, url_for, request
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from datetime import datetime
from flask_bcrypt import Bcrypt


from utils.get_data_from_excel import get_headers_from_excel, get_data_from_excel
from utils.map_creator import MapCreator

# create Flask app instance
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '1234567891011123142adjhbakdhajsjdhabjhcbakjsajhcb'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<User: {self.username}>"
    

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.Date, default=datetime.utcnow)

    user = relationship('User')

    def __repr__(self):
        return f"<Map: {self.id}>"
    

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
        

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route("/")
def index():
    # render index page
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route("/api/get_map/", methods=["POST"])
def get_map():
    # Check for file
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 200

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 200

    if ".xlsx" not in file.filename:
        return jsonify({"error": "This not excel file!"}), 200

    # get data from request
    label = request.form["label"]
    lat = request.form["lat"]
    lon = request.form["lon"]
    icon = request.form["icon"]
    color = request.form["color"]
    unique_labels = request.form["unique_labels"]
    unique_labels = True if unique_labels == "true" else False

    # getting data from Excel file
    marker_data = get_data_from_excel(file, label, lat, lon, unique_labels)
    if not marker_data:
        return jsonify({"error": "No valid data"}), 200
    # create map and add layers to map
    map_creator = MapCreator(marker_data, icon, color)
    map_creator.add_deepstate_layer()
    map_creator.add_region_layer()
    map_creator.add_points()
    map_creator.add_fullscreen_btn()
    map_creator.add_layer_control()

    # create map html version
    map_html = map_creator.m.get_root().render()

    # return html map
    return jsonify(
        {
            "map_html": map_html,
        }
    )


@app.route("/api/get_headers/", methods=["POST"])
def get_headers():
    # check file is valid
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 200

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 200

    if ".xlsx" not in file.filename:
        return jsonify({"error": "This not excel file!"}), 200

    # get headers from excel file
    headers = get_headers_from_excel(file)
    return {"headers": headers}
