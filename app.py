from flask import Flask
from flask import render_template, request, jsonify

from utils.get_data_from_excel import get_headers_from_excel, get_data_from_excel
from utils.map_creator import MapCreator

# create Flask app instance
app = Flask(__name__)


@app.route("/")
def index():
    # render index page
    return render_template("index.html")


@app.route("/api/get_map/", methods=["POST"])
def get_map():
    # Check for file
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if ".xlsx" not in file.filename:
        return "This not excel file!", 400

    # get data from request
    label = request.form["label"]
    lat = request.form["lat"]
    lon = request.form["lon"]
    icon = request.form["icon"]
    color = request.form["color"]
    unique_labels = request.form["unique_labels"]
    unique_labels = True if unique_labels == 'true' else False

    # getting data from excel file
    marker_data = get_data_from_excel(file, label, lat, lon, unique_labels)

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
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if ".xlsx" not in file.filename:
        return "This not excel file!", 400

    # get headers from excel file
    headers = get_headers_from_excel(file)
    return {"headers": headers}


if __name__ == "__main__":
    app.run()
