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
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import *

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

  search_term = request.form.get('search_term', '')
  venue = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  response = {
    "count": len(venue),
    "data": venue
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = Venue.query.get(venue_id)

  if not venue:
    return not_found_error('Venue not found.')

  today = datetime.now()
  upcoming_shows_query = Show.query.join(Artist).filter(Show.venue_id == venue.id).filter(Show.start_time > today).all()
  past_shows_query = Show.query.join(Artist).filter(Show.venue_id == venue.id).filter(Show.start_time < today).all()
  
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


#  Delete Venue
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

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

  return render_template('pages/home.html', data = venue)

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  data = Artist.query.with_entities(Artist.id, Artist.name)

  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get('search_term', '')
  artist = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  response = {
    "count": len(artist),
    "data": artist
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.get(artist_id)

  if not artist:
    return not_found_error('Artist not found.')

  today = datetime.now()
  upcoming_shows_query = Show.query.join(Venue).filter(Show.artist_id == artist.id).filter(Show.start_time > today).all()
  past_shows_query = Show.query.join(Venue).filter(Show.artist_id == artist.id).filter(Show.start_time < today).all()
  
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
  
  artist = Artist.query.filter_by(id = artist_id).first()

  if not artist:
    return not_found_error('Artist not found.')

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

  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

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

  venue = Venue.query.get(venue_id)

  if not venue:
    return not_found_error('Venue not found.')

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

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

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

  data = []
  shows = Show.query.join(Artist).join(Venue).all()
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
    
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error = ''):
    return render_template('errors/404.html', error = error), 404

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

