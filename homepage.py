#run "C:/Vs Code/uni/sa/.venv/bin/activate.bat"
from flask import Flask, render_template, session, redirect, url_for
from labpage import lab_bp
from product import product_bp
from labworker import labworker_bp
from scientist import scientist_bp
from login import login_bp  # login blueprint
from report import report_bp
from scientist import scientist_bp

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_12345'

# Register blueprints
app.register_blueprint(lab_bp)
app.register_blueprint(product_bp)
app.register_blueprint(labworker_bp)
app.register_blueprint(scientist_bp)
app.register_blueprint(login_bp)
app.register_blueprint(report_bp)

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login.login"))
    return render_template("index.html", username=session["user"], role=session.get("role","user"))

if __name__ == "__main__":
    app.run(debug=True)
