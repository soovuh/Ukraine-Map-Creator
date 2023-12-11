import folium
import requests
import json

from folium import plugins

# Here i need to change from 1 layer to more layers
class MapCreator:
    def __init__(self):
        self.m = folium.Map(
            prefer_canvas=True,
            zoom_start=7,
            tiles=None,
            name="My Ukraine map",
        )
        (
            folium.TileLayer(
                tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                attr="Custom tiles",
                name="Map",
            ).add_to(self.m)
        )

    def add_deepstate_layer(self):
        url = "https://deepstatemap.live/api/history/1699478008/geojson"
        raw_data = requests.get(url).json()
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                feature
                for feature in raw_data["features"]
                if feature["geometry"]["type"] != "Point"
            ],
        }

        geojson_layer = folium.GeoJson(
            data=geojson_data,
            name="deepstate",
            style_function=lambda x: {
                "fillColor": x["properties"]["fill"],
                "color": x["properties"]["stroke"],
                "weight": x["properties"]["stroke-width"],
                "fillOpacity": x["properties"]["fill-opacity"],
            },
        )
        deepstate_layer = folium.FeatureGroup("Deep State").add_to(self.m)
        geojson_layer.add_to(deepstate_layer)

    def add_region_layer(self):
        file = open("static/json/regions.geojson")
        raw_data = json.load(file)
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                feature
                for feature in raw_data["features"]
                if feature["geometry"]["type"] != "Point"
            ],
        }

        geojson_layer = folium.GeoJson(
            data=geojson_data,
            name="regions",
            style_function=lambda x: {"fillOpacity": 0, "weight": 1},
        )
        region_layer = folium.FeatureGroup("Regions").add_to(self.m)
        geojson_layer.add_to(region_layer)

    def add_points_layer(self, layer):
        markers_layer = folium.FeatureGroup("Markers").add_to(self.m)
        for entry in layer["data"]:
            text_label = entry["label"]
            coords = entry["coords"]
            folium.Marker(
                location=coords,
                popup=text_label,
                icon=folium.Icon(icon=layer["icon"], prefix="fa", color=layer["color"]),
            ).add_to(markers_layer)
            label_html = (
                f"<div style='text-align: center; color: black; font-weight: bold; transform: translate("
                f"-50%, -300%); font-size: 1.3em;'>{text_label}</div>"
            )
            label = folium.Marker(
                location=coords, icon=folium.DivIcon(icon_size=(0, 0), html=label_html)
            )
            label.add_to(markers_layer)

    def add_fullscreen_btn(self):
        plugins.Fullscreen(
            position="bottomright",
            title="Expand me",
            title_cancel="Exit me",
            force_separate_button=True,
        ).add_to(self.m)

    def add_layer_control(self):
        folium.LayerControl().add_to(self.m)
