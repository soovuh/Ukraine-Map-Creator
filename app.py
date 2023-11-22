import tempfile

from flask import Flask
from flask import render_template, request, jsonify

from utils.get_data_from_excel import get_headers_from_excel, get_data_from_excel
from utils.map_creator import MapCreator
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get_map/', methods=['POST'])
def get_map():
    # Check for file
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if '.xlsx' not in file.filename:
        return 'This not excel file!', 400

    # get data from request
    label = request.form['label']
    lat = request.form['lat']
    lon = request.form['lon']
    icon = request.form['icon']
    color = request.form['color']

    # getting data from excel file
    marker_data = get_data_from_excel(file, label, lat, lon)

    # create map and add layers to map
    map_creator = MapCreator(marker_data, icon, color)
    map_creator.add_deepstate_layer()
    map_creator.add_region_layer()
    map_creator.add_points()
    map_creator.add_fullscreen_btn()

    # create map html version
    map_html = map_creator.m.get_root().render()

    # return html map
    return jsonify({
        'map_html': map_html,
    })


@app.route('/api/get_headers/', methods=['POST'])
def get_headers():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if '.xlsx' not in file.filename:
        return 'This not excel file!', 400

    headers = get_headers_from_excel(file)
    return {
        'headers': headers
    }


if __name__ == '__main__':
    app.run()
