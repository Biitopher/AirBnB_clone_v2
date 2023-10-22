#!/usr/bin/python3
"""Script starting flask web applicaton"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
import os
from shutil import copyfile
app = Flask(__name__)


static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "web_flask/static")


@app.teardown_appcontext
def close_storage(exception):
    """Close the current SQLAlchemy session."""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display an HTML page with filters for States, Cities, and Amenities."""
    css_files = ["3-footer.css", "3-header.css", "4-common.css",
                 "6-filters.css"]
    for css_file in css_files:
        source_css = os.path.join("web_static/styles", css_file)
        destination_css = os.path.join(static_dir, "styles", css_file)
        copyfile(source_css, destination_css)

    image_files = ["icon.png", "logo.png"]
    for image_file in image_files:
        source_img = os.path.join("web_static/images", image_file)
        destination_img = os.path.join(static_dir, "images", image_file)
        copyfile(source_img, destination_img)

    states = storage.all(State).values()
    cities = []

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        cities = [city for state in states for city in state.cities]
    else:
        for state in states:
            cities.extend(state.cities)

    states = sorted(states, key=lambda state: state.name)
    cities = sorted(cities, key=lambda city: city.name)

    for obj in [states, cities, storage.all(Amenity).values()]:
        for item in obj:
            item.name = "&nbsp;"

    return render_template(
        '10-hbnb_filters.html',
        states=states,
        cities=cities,
        amenities=storage.all(Amenity).values()
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
