#!/usr/bin/python3
"""script that starts a Flask web application"""

import models
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a list of all State objects sorted by name."""
    states = storage.all(State).values()
    sorted_states = sorted(list(states),
                           key=lambda state: state.name)

    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage engine (FileStorage or DBStorage)."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
