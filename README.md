# Ukraine Map Creator

The "Ukraine Map Creator" is a web application that allows users to generate customized maps with markers based on location data. This project utilizes Flask, SQLAlchemy, Folium, Bootstrap, and pandas to provide a seamless and intuitive mapping experience.

## Technology Stack

- **Flask**: Web framework for building the application.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) for database interactions.
- **Folium**: Library for visualizing geospatial data.
- **Bootstrap**: Front-end framework for responsive and mobile-first web development.
- **pandas**: Data manipulation and analysis library for handling uploaded XLSX files.

## Key Features

- **Map Creation**: Upload XLSX files containing latitude, longitude, and marker labels to create maps.
- **Column Flexibility**: Easily select column names corresponding to location data during the upload process.
- **Label Uniqueness**: Choose whether label uniqueness is important for your map.
- **Customization**: Customize marker icons and colors to personalize your maps.
- **Download Options**: Download maps as HTML files or take snapshot images for offline use.
- **User Dashboard**: Registered users can save maps to their dashboard for easy access.

## Getting Started

To get started with the "Ukraine Map Creator", follow these steps:

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Access the application in your web browser at `http://localhost:5000`

## Usage

1. Upload your XLSX file containing location data.
2. Select the appropriate column names for latitude, longitude, and labels.
3. Customize marker icons and colors as desired.
4. Choose whether label uniqueness is important for your map.
5. Download your map as an HTML file or take a snapshot image.
6. Registered users can also save maps to their dashboard for future access.


