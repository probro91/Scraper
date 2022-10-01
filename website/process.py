from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    print(request.form)
    print(request.form.get("account"))
    return render_template("base.html")