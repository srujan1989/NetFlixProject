from flaskapp.config import db, ma


# Netflix Model Class
class Netflix(db.Model):
    show_id = db.Column(db.Integer, primary_key=True)
    show_type = db.Column(db.String(50))
    title = db.Column(db.String(100))
    director = db.Column(db.String(100))
    cast = db.Column(db.String(250))
    country = db.Column(db.String(50))
    date_added = db.Column(db.String(50))
    release_year = db.Column(db.Integer)
    rating = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    listed_in = db.Column(db.String(100))
    description = db.Column(db.String(250))

    def __init__(self, show_id, show_type, title, director, cast, country, date_added, release_year, rating, duration,
                 listed_in, description):
        self.show_id = show_id
        self.show_type = show_type
        self.title = title
        self.director = director
        self.cast = cast
        self.country = country
        self.date_added = date_added
        self.release_year = release_year
        self.rating = rating
        self.duration = duration
        self.listed_in = listed_in
        self.description = description


# Netflix Schema Class
class NetflixSchema(ma.Schema):
    class Meta:
        fields = ('show_id', 'show_type', 'title', 'director', 'cast', 'country', 'date_added', 'release_year',
                  'rating', 'duration', 'listed_in',  'description')
