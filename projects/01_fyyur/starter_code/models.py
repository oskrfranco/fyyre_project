from app import db

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