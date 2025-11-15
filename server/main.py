from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello from server!</h1>"

@app.route("/hello")
def hello():
    return "<h1>Hello</h1>"

@app.route("/greeting/<name>")
def greeting(name):
    return f"<h1>Greeting, {name}!</h1>"

@app.route("/add/<int:number1>/<int:number2>")
def add(number1, number2):
    result = number1+number2
    return f"{number1} + {number2} = {result}"

@app.route("/handle_url_params")
def handle_url_params():
    param1 = request.args.get("param1", "default1")
    param2 = request.args.get("param2", "default2")
    return f"Param1: {param1}, Param2: {param2}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)