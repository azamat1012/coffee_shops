from flask import Flask
import os

CURRENT_PATH = os.path.dirname(__file__)
MAP_PATH = f"{CURRENT_PATH}/coffee_map.html"

def start():
    with open(MAP_PATH, "r") as file:
        return file.read()

app = Flask(__name__)
app.add_url_rule("/", "main", start)

if __name__ == "__main__":
    app.run("0.0.0.0")
