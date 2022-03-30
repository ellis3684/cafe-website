from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL
import os

# Set up Flask with Flask Bootstrap, Flask Moment, and random app secret key config
app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Set API Key required to delete cafes
API_KEY = os.environ.get('DELETE_CAFE_API_KEY')

# Connect to SQLite database
uri = os.environ.get('DATABASE_URL', "sqlite:///cafes.db")
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
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


# db.create_all()


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


# Home route renders all cafes in db
@app.route('/')
def home():
    cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=cafes)


# Add cafe form uses Flask form to post new cafe to db
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
        flash(f'Cafe \'{new_cafe.name}\' successfully added!', 'success')
        return redirect(url_for('home'))
    return render_template('add-cafe.html', form=form)


# Search for cafe via location
@app.route('/search')
def search_by_location():
    location = request.args.get('loc').title()
    cafes_in_area = Cafe.query.filter_by(location=location).all()
    if not cafes_in_area:
        flash(f'Oh no! It looks like we don\'t have any cafes in {location}.', 'failure')
    return render_template('index.html', cafes=cafes_in_area)


# App route once edit to cafe is made, redirects to home once complete
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


# User can delete cafes in db only if they have the API key required
@app.route('/delete', methods=['GET', 'POST'])
def delete_cafe():
    if request.method == 'GET':
        cafe_name = request.args.get('name')
        cafe_id = request.args.get('id')
        return render_template('delete.html', cafe_name=cafe_name, cafe_id=cafe_id)
    elif request.method == 'POST':
        if request.form['api_key'] == API_KEY:
            cafe_id = request.form['id']
            cafe = Cafe.query.get(cafe_id)
            name = cafe.name
            db.session.delete(cafe)
            db.session.commit()
            flash(f'Cafe \'{name}\' successfully deleted.', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'That\'s not a valid key. Please note that if you do not '
                  f'have a valid API key you will not be able to delete cafes from Sip Spots.', 'failure')
            return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
