from flask import Flask, redirect, url_for
from user.routes import user_bp
from admin.routes import admin_bp
from flask_session import Session
from config import Config
from models import db
import os
 
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config.from_object(__name__)
Session(app)

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route("/")
def home():
    return redirect(url_for('user_bp.login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
    #app.run(debug=True)
