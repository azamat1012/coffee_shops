import os
from flask import Flask

app = Flask(__name__)
CURRENT_PATH = os.path.dirname(__file__)
MAP_PATH = f"{CURRENT_PATH}/coffee_map.html"

@app.route("/")
def start():
    with open(MAP_PATH, "r") as file:
        return file.read()

if __name__ == "__main__":
    app.run("0.0.0.0")
