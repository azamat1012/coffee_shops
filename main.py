import os
from flask import Flask

CURRENT_PATH = os.path.dirname(__file__)
MAP_PATH = f"{CURRENT_PATH}/coffee_map.html"

app = Flask(__name__)

def start():
    with open(MAP_PATH, "r") as file:
        return file.read()

app.add_url_rule("/", "main", start)

if __name__ == "__main__":
    app.run("0.0.0.0")
