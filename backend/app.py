from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="static")

# Serve index.html for root URL

@app.route("/test")
def test():
    import os
    return jsonify({"files_in_static": os.listdir(app.static_folder)})

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")



# App configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-this-secret")

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import models AFTER defining app
from models import db, User

# Bind SQLAlchemy to Flask app
db.init_app(app)

# Create tables if not existing
with app.app_context():
    db.create_all()

@app.route("/<path:filename>")
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)

# ✅ -------- REGISTER ROUTE --------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    fname = data.get("fname","").strip()
    lname = data.get("lname","").strip()
    email = data.get("email","").strip()
    mobile = data.get("mobile","").strip()
    password = data.get("password","").strip()
    confirmPassword = data.get("confirmPassword","").strip()

    print(f"Received registration data: fname={fname}, lname={lname}, email={email}, mobile={mobile}")
    # Validate inputs
    if not fname or not lname or not email or not mobile or not password or not confirmPassword:
        return jsonify({"error": "All fields are required"}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Hash password and save user
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(fname=fname, lname=lname, email=email, mobile=mobile, password=hashed_password, confirmPassword=confirmPassword,registered=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 200

# ✅ -------- LOGIN ROUTE --------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=user.email)
        return jsonify({"message": "Login successful!", "token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users_list = []
    for u in users:
        users_list.append({
            "id": u.id,
            "fname": u.fname,
            "lname": u.lname,
            "email": u.email,
            "mobile": u.mobile,
            "registered": u.registered
        })
    return jsonify(users_list)

# ✅ -------- PROTECTED EXAMPLE ROUTE --------
@app.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome {current_user}!"}), 200
print("Static folder absolute path:", os.path.abspath(app.static_folder))
print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(rule)


# ✅ Run server
# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

