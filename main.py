from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


# Set up Flask
app = Flask(__name__)
moment = Moment(app)

# Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe table config
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


# Home route
@app.route('/')
def home():
    cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=cafes)


@app.route('/add-cafe')
def add_cafe():
    return render_template('add-cafe.html')


if __name__ == '__main__':
    app.run(debug=True)



