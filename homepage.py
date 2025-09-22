from flask import Flask, render_template
from labpage import lab_bp
from product import product_bp
from labworker import labworker_bp
from labmicro import micro_bp
from labchem import chem_bp

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_12345'

app.register_blueprint(lab_bp)
app.register_blueprint(product_bp)
app.register_blueprint(labworker_bp)
app.register_blueprint(micro_bp)
app.register_blueprint(chem_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

