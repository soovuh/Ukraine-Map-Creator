import folium
import requests
import json

from folium import plugins


class MapCreator:
    def __init__(self, data, icon, color):
        self.data = data
        self.icon = icon
        self.color = color
        self.center = self.average_coords()
        self.m = folium.Map(
            location=self.center,
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
        file = open("static/json/deep.geojson")
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

    def add_points(self):
        markers_layer = folium.FeatureGroup("Markers").add_to(self.m)
        for entry in self.data:
            text_label = entry["label"]
            coords = entry["coords"]
            folium.Marker(
                location=coords,
                popup=text_label,
                icon=folium.Icon(icon=self.icon, prefix="fa", color=self.color),
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

    def average_coords(self):
        sum_lat = 0
        sum_lon = 0

        for entry in self.data:
            coords = entry["coords"]
            sum_lat += coords[0]
            sum_lon += coords[1]

        avg_lat = sum_lat / len(self.data)
        avg_lon = sum_lon / len(self.data)

        return avg_lat, avg_lon

    # Function for updating data if user have only places names in xlsx file
    def get_coords_with_place(self):
        pass
