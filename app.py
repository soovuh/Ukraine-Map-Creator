from flask import Flask
import os
from flask import render_template, jsonify, redirect, url_for, request
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)

from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from utils.get_data_from_excel import get_headers_from_excel, get_data_from_excel
from utils.map_creator import MapCreator
from utils.generate_unique_code import generate_unique_code


from models import db, User, Map
from forms import LoginForm, RegisterForm

# create Flask app instance
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "1234567891011123142adjhbakdhajsjdhabjhcbakjsajhcb"


db.init_app(app)
bcrypt = Bcrypt(app)
admin = Admin(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Map, db.session))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/create")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_maps = Map.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", maps=user_maps)


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
    ), 200


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


@app.route("/api/save/", methods={"POST"})
@login_required
def save():
    id = current_user.id
    unique_code = generate_unique_code()
    file_name = f'{id}_{unique_code}.html'
    data = request.get_json()
    html_data = data["html_data"]
    with open(f'/static/media/{file_name}', 'w') as file:
        file.write(html_data)
    new_map = Map(user_id=id, html=f'/static/media/{file_name}')
    db.session.add(new_map)
    db.session.commit()
    return jsonify({"success": "success"}), 200


@app.route('/api/get_html_map/<int:map_id>/')
def get_html_map(map_id):
    map_data = Map.query.get(map_id)

    if map_data:
        return jsonify({"html": map_data.html, "name": f"{map_data.id}_{map_data.date_created}"})
    else:
        return jsonify({"error": "Map not found"}), 404


@app.route('/api/delete_map/<int:map_id>/')
def delete_map(map_id):
    map_data = Map.query.get(map_id)

    if map_data:
        os.remove(f'static/media/{map_data.html}')
        db.session.delete(map_data)
        db.session.commit()
        return jsonify({"message": "Map deleted successfully"})
    else:
        return jsonify({"error": "Map not found"}), 404

@app.route('/')
def info():
    return render_template("info.html")
    
# run app command
# flask --app app run --debug