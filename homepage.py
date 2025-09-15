from flask import Flask, render_template
from labpage import lab_bp
from product import product_bp

app = Flask(__name__)
app.register_blueprint(lab_bp)
app.register_blueprint(product_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

