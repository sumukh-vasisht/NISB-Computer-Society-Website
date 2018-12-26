from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    slides = [
        "slide1.jpg",
        "slide2.jpg"
    ]
    return render_template("index.html", slides=slides)

if __name__=="__main__":
    app.run(debug=True)