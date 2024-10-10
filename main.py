from flask import Flask
import os

current_path = os.path.dirname(__file__)


def start():
    with open(f"{current_path}/coffee_map.html", "r") as file:
        return file.read()


app = Flask(__name__)
app.add_url_rule("/", "main", start)

if __name__ == "__main__":
    app.run("0.0.0.0")
