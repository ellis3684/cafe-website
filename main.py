from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL
import os


# Set up Flask
app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


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


# Config flask form to add cafes
class AddCafeForm(FlaskForm):
    cafe = StringField('Cafe name:', validators=[DataRequired()])
    map_url = URLField('Cafe location on Google Maps (URL):', validators=[DataRequired(), URL()])
    image_url = URLField('Cafe seating area image (URL):', validators=[DataRequired(), URL()])
    location = StringField('Cafe location (which part of the city):', validators=[DataRequired()])
    coffee_price = StringField('Price for a coffee in local currency:', validators=[DataRequired()])
    seats = StringField('How many seats are available?', validators=[DataRequired()])
    wifi = BooleanField('Is there WiFi?')
    socket = BooleanField('Are there sockets for your laptop or phone?')
    toilet = BooleanField('Is there a restroom?')
    calls_ok = BooleanField('Can you take business calls here?')
    submit = SubmitField('Submit')


# Home route
@app.route('/')
def home():
    cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=cafes)


@app.route('/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.data['cafe'],
            map_url=form.data['map_url'],
            img_url=form.data['image_url'],
            location=form.data['location'],
            seats=form.data['seats'],
            has_toilet=form.data['toilet'],
            has_wifi=form.data['wifi'],
            has_sockets=form.data['socket'],
            can_take_calls=form.data['calls_ok'],
            coffee_price=form.data['coffee_price'],
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add-cafe.html', form=form)


@app.route('/search')
def search_by_location():
    location = request.args.get('loc').title()
    cafes_in_area = Cafe.query.filter_by(location=location).all()
    if not cafes_in_area:
        flash(f'Oh no! It looks like we don\'t have any cafes in {location}.')
    return render_template('index.html', cafes=cafes_in_area)


@app.route('/edit', methods=['POST'])
def edit_cafe():
    cafe_id = request.form['id']
    cafe = Cafe.query.get(cafe_id)
    cafe.name = request.form['name']
    cafe.location = request.form['location']
    cafe.map_url = request.form['maps_url']
    cafe.img_url = request.form['img_url']
    cafe.coffee_price = request.form['coffee_price']
    cafe.seats = request.form['seats']
    cafe.has_toilet = bool(request.form['has_toilet'])
    cafe.has_wifi = bool(request.form['has_wifi'])
    cafe.has_sockets = bool(request.form['has_sockets'])
    cafe.can_take_calls = bool(request.form['can_take_calls'])
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)



