from sqlite3 import IntegrityError

from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class TypePlace(db.Model):
    __tablename__ = 'type_place'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mood = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<TypePlace {self.name}>'


# Define the Place model
class Place(db.Model):
    __tablename__ = 'place'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    points = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Place {self.name}>'


# Define the Users model
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    id_telegram = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)

    # Relationship to Place
    places = db.relationship('Place', backref='user', lazy=True)

    def __repr__(self):
        return f'<Users {self.id_telegram}>'

# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/capture_id', methods=['POST'])
def capture_id():
    data = request.json
    id_telegram = data.get('id_telegram')

    if not id_telegram:
        return jsonify({"error": "id_telegram is required"}), 400

    # Create a new user entry
    new_user = Users(id_telegram=id_telegram)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "id_telegram captured successfully"}), 201


@app.route('/capture_ip', methods=['GET'])
def capture_ip():
    id_telegram = request.args.get('id_telegram')
    user_ip = request.remote_addr

    if not id_telegram:
        return jsonify({"error": "id_telegram is required"}), 400

    # Update the existing user entry with the IP address
    user = Users.query.filter_by(id_telegram=id_telegram).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    user.ip_address = user_ip

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

    # Send a message to the bot with a link to interact again
    print(user_ip)
    print(request.post(f"https://locator.api.maps.yandex.ru/v1/locate?apikey={os.environ['YANDEX_MAPS_KEY']}", {"ip":[{"address":user_ip}]}))
    # You can store the bot message in a variable or send it directly to the bot here
    # return jsonify({"ip":[{"address":user_ip}]})
    return redirect("https://t.me/" + os.environ["BOT_TAG"], 301)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)