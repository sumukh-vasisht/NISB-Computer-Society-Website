from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def index():    
    return render_template("index.html")
    
@app.route("/Home")
def home():    
    return render_template("home.html")
    
@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/Events")
def events():
    return render_template("events.html")

@app.route("/Rubix")
def rubix():
    return render_template("rubix.html")

@app.route("/Contact")
def contact():
    return render_template("contact.html")

if __name__=="__main__":
    app.run(debug=True)