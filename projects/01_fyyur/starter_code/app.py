#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#COMPLETED# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(200))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    past_shows = db.Column(db.String(500))
    upcoming_shows = db.Column(db.String(500))
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)
    venue_shows = db.relationship('Show', backref = 'show_venue', cascade='all,delete')

    #COMPLETED# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    looking_for_venues = db.Column(db.Boolean(), nullable=False, default=False)
    looking_for_description = db.Column(db.String(500))
    artist_shows = db.relationship('Show', backref = 'show_artist', cascade='all,delete')

    #COMPLETED# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key = True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  start_time = db.Column(db.DateTime, nullable = False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  recent_artists = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.name.asc()).limit(10).all()
  recent_venues = Venue.query.with_entities(Venue.id, Venue.name).order_by(Venue.name.asc()).limit(10).all()

  return render_template('pages/home.html', artists = recent_artists, venues = recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #COMPLETED# TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]

  venues_cities = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).order_by(Venue.state.asc(), Venue.city.asc()).all()
  data = []
  today = datetime.now()
  for venue_city in venues_cities:
    venue_city_data = {}
    venue_city_data['city']  = venue_city.city
    venue_city_data['state'] = venue_city.state
    venue_city_data['venues'] = []
    city_venues = Venue.query.with_entities(Venue.id, Venue.name).filter_by(city = venue_city.city).all()

    for city_venue in city_venues:
      venue_shows = Show.query.filter(Show.venue_id == city_venue.id).filter(Show.start_time > today).all()
      city_venues_data = {
        "id": city_venue.id,
        "name": city_venue.name,
        "num_upcoming_shows": len(venue_shows)
      }
      venue_city_data['venues'].append(city_venues_data)
    data.append(venue_city_data)


  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  #COMPLETED# TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  #COMPLETED# seach for Hop should return "The Musical Hop".
  #COMPLETED# search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  search_term = request.form.get('search_term', '')
  venue = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  response = {
    "count": len(venue),
    "data": venue
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  #COMPLETED# TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  venue = Venue.query.get(venue_id)
  today = datetime.now()
  upcoming_shows_query = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time > today).all()
  past_shows_query = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time < today).all()
  
  upcoming_shows_data = []
  for upcoming_show in upcoming_shows_query:
    show_data = {
      "artist_id": upcoming_show.show_artist.id,
      "artist_name": upcoming_show.show_artist.name,
      "artist_image_link": upcoming_show.show_artist.image_link,
      "start_time": upcoming_show.start_time.strftime("%Y/%m/%d, %H:%M:%S")
    }
    upcoming_shows_data.append(show_data)

  past_shows_data = []
  for past_show in past_shows_query:
    show_data = {
      "artist_id": past_show.show_artist.id,
      "artist_name": past_show.show_artist.name,
      "artist_image_link": past_show.show_artist.image_link,
      "start_time": past_show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    past_shows_data.append(show_data)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres.split(","),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows_data,
    "upcoming_shows": upcoming_shows_data,
    "past_shows_count": len(past_shows_query),
    "upcoming_shows_count": len(upcoming_shows_query)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  #COMPLETED# TODO: insert form data as a new Venue record in the db, instead
  error = False

  if 'seeking_talent' in request.form:
    is_seeking_talent = True
  else:
    is_seeking_talent = False

  seeking_talent_description = ''
  if 'seeking_description' in request.form:
    seeking_talent_description = request.form['seeking_description']

  try:
    venue_name = request.form['name']
    city =            request.form['city']
    state =           request.form['state']
    address =         request.form['address']
    phone =           request.form['phone']
    genres =          ','.join(map(str, request.form.getlist('genres')))
    facebook_link =   request.form['facebook_link']
    image_link =      request.form['image_link']
    website_link =    request.form['website_link']
    seeking_talent =  is_seeking_talent
    seeking_description = seeking_talent_description

    venue = Venue(
      name = venue_name,
      city = city,
      state = state,
      address = address,
      phone = phone,
      genres = genres,
      facebook_link = facebook_link,
      image_link = image_link,
      website = website_link,
      seeking_talent = seeking_talent,
      seeking_description = seeking_description
    )
    db.session.add(venue)
    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    error = True
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if not error:
    return render_template('pages/home.html', data = Venue)

  #COMPLETED# TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  #COMPLETED# TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html', data = Venue)


#  Delete Venue
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  #COMPLETED# TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.filter_by(id = venue_id).first()
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully deleted.')
  except:
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html', data = venue)

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  #COMPLETED# TODO: replace with real data returned from querying the database
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]

  data = Artist.query.with_entities(Artist.id, Artist.name)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  #COMPLETED# TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  search_term = request.form.get('search_term', '')
  artist = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  response = {
    "count": len(artist),
    "data": artist
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  #COMPLETED# TODO: replace with real artist data from the artist table, using artist_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  artist = Artist.query.get(artist_id)

  today = datetime.now()
  upcoming_shows_query = Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time > today).all()
  past_shows_query = Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time < today).all()
  
  upcoming_shows_data = []
  for upcoming_show in upcoming_shows_query:
    show_data = {
      "venue_id": upcoming_show.show_venue.id,
      "venue_name": upcoming_show.show_venue.name,
      "venue_image_link": upcoming_show.show_venue.image_link,
      "start_time": upcoming_show.start_time.strftime("%Y/%m/%d, %H:%M:%S")
    }
    upcoming_shows_data.append(show_data)

  past_shows_data = []
  for past_show in past_shows_query:
    show_data = {
      "venue_id": past_show.show_venue.id,
      "venue_name": past_show.show_venue.name,
      "venue_image_link": past_show.show_venue.image_link,
      "start_time": past_show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    past_shows_data.append(show_data)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "seeking_venue": artist.looking_for_venues,
    "seeking_description": artist.looking_for_description,
    "image_link": artist.image_link,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "past_shows": past_shows_data,
    "upcoming_shows" : upcoming_shows_data,
    "past_shows_count": len(past_shows_query),
    "upcoming_shows_count": len(upcoming_shows_query)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  
  artist = Artist.query.filter_by(id = artist_id).first()
  form = ArtistForm(
    name = artist.name,
    city = artist.city,
    state = artist.state,
    phone = artist.phone,
    genres = artist.genres.split(','),
    facebook_link = artist.facebook_link,
    image_link = artist.image_link,
    website_link = artist.website,
    seeking_venue = artist.looking_for_venues == True,
    seeking_description = artist.looking_for_description
  )

  #COMPLETED# TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  #COMPLETED# TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = Artist.query.get(artist_id)
    artist.name =   request.form.get('name', '')
    artist.city =   request.form.get('city', '')
    artist.state =  request.form.get('state', '')
    artist.phone =  request.form.get('phone', '')
    artist.genres = ','.join(map(str, request.form.getlist('genres')))
    artist.facebook_link = request.form.get('facebook_link' , '')
    artist.image_link = request.form.get('image_link', '')
    artist.website = request.form.get('website_link', '')
    artist.looking_for_venues = request.form.get('seeking_venue') == 'y'
    artist.looking_for_description = request.form.get('seeking_description', '')

    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }

  venue = Venue.query.get(venue_id)
  form = VenueForm(
    name = venue.name,
    city = venue.city,
    state = venue.state,
    address = venue.address,
    phone = venue.phone,
    genres = venue.genres.split(','),
    facebook_link = venue.facebook_link,
    image_link = venue.image_link,
    website_link = venue.website,
    seeking_talent = venue.seeking_talent == True,
    seeking_description = venue.seeking_description
  )

  #COMPLETED# TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  #COMPLETED# TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  try:
    venue = Venue.query.get(venue_id)
    venue.name =      request.form.get('name', '')
    venue.city =      request.form.get('city', '')
    venue.state =     request.form.get('state', '')
    venue.address =   request.form.get('address', '')
    venue.phone =     request.form.get('phone', '')
    venue.genres =    ','.join(map(str, request.form.getlist('genres')))
    venue.facebook_link = request.form.get('facebook_link', '')
    venue.image_link =    request.form.get('image_link', '')
    venue.website =       request.form.get('website_link', '')
    venue.seeking_talent = request.form.get('seeking_talent') == 'y'
    venue.seeking_description = request.form.get('seeking_description')

    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  #COMPLETED# TODO: insert form data as a new Venue record in the db, instead
  #COMPLETED# TODO: modify data to be the data object returned from db insertion

  error = False

  if 'seeking_venue' in request.form:
    is_seeking_venue = True
  else:
    is_seeking_venue = False

  seeking_venue_description = ''
  if 'seeking_description' in request.form:
    seeking_venue_description = request.form['seeking_description']

  try:
    name =            request.form['name']
    city =            request.form['city']
    state =           request.form['state']
    phone =           request.form['phone']
    genres =          ','.join(map(str, request.form.getlist('genres')))
    facebook_link =   request.form['facebook_link']
    image_link =      request.form['image_link']
    website_link =    request.form['website_link']
    looking_for_venues =  is_seeking_venue
    looking_for_description = seeking_venue_description

    artist = Artist(
      name = name,
      city = city,
      state = state,
      phone = phone,
      genres = genres,
      facebook_link = facebook_link,
      image_link = image_link,
      website = website_link,
      looking_for_venues = looking_for_venues,
      looking_for_description = looking_for_description
    )
    db.session.add(artist)
    db.session.commit()

    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    error = True
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if not error:
    return render_template('pages/home.html', data = Artist)

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  #COPMLETED# TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #return render_template('pages/home.html')

#  Delete Artist
#  ----------------------------------------------------------------

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  try:
    artist = Artist.query.filter_by(id = artist_id).first()
    db.session.delete(artist)
    db.session.commit()
    flash('Artist ' + artist.name + ' was successfully deleted.')
  except:
    flash('An error occurred. Artist ' + artist.name + ' could not be deleted.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return render_template('pages/home.html', data = artist)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  #COMPLETED# TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]

  data = []
  shows = Show.query.all()
  for show in shows:
    show_data = {
      "venue_id": show.show_venue.id,
      "venue_name": show.show_venue.name,
      "artist_id": show.show_artist.id,
      "artist_name": show.show_artist.name,
      "artist_image_link": show.show_artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    data.append(show_data)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  #COMPLETED# TODO: insert form data as a new Show record in the db, instead

  try:
    form_venue_id = request.form.get('venue_id', '')
    venue = Venue.query.filter_by(id = form_venue_id).first()
    form_artist_id = request.form.get('artist_id', '')
    artist = Artist.query.filter_by(id = form_artist_id).first()
    show = Show(
      show_artist = artist,
      show_venue = venue,
      start_time = request.form.get('start_time', '')
    )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  #COMPLETED# TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
'''
# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

