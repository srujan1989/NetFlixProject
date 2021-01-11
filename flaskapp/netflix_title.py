import logging
from flask import request, jsonify, abort
from sqlalchemy import or_, exc
from flaskapp.models import Netflix, NetflixSchema
from flaskapp.config import app, db


# Init Marshmallow Schemas
netflix_title_schema = NetflixSchema()
netflix_titles_schema = NetflixSchema(many=True)


# Get all Netflix Titles
@app.route('/netflix', methods=['GET'])
def get_netflix_titles():

    # Get all the Query String Params
    args = request.args

    # Get the page and size (used for pagination)
    page = int(args.get('page', 1))
    size = int(args.get('size', 20))

    # Get the search QS param, used to search based on key word in any column
    search = args.get('search')

    # Get the field on which it should be sorted, by default it will sorted on show_id ascending
    sort_by_field = args.get('sort_by_field', 'show_id')
    sort_order = args.get('sort_order', 'asc')

    netflix_titles_query = Netflix.query

    if search:
        search = '%{}%'.format(search)
        netflix_titles_query = netflix_titles_query.filter(
            or_(
                Netflix.show_id.like(search),
                Netflix.show_type.like(search),
                Netflix.title.like(search),
                Netflix.director.like(search),
                Netflix.cast.like(search),
                Netflix.country.like(search),
                Netflix.date_added.like(search),
                Netflix.release_year.like(search),
                Netflix.rating.like(search),
                Netflix.duration.like(search),
                Netflix.listed_in.like(search),
                Netflix.description.like(search),
            )
        )

    if sort_by_field and sort_order == 'desc':
        sort_by = getattr(Netflix, sort_by_field).desc()
    else:
        sort_by = getattr(Netflix, sort_by_field).asc()

    netflix_titles = netflix_titles_query.order_by(sort_by).paginate(page, size, error_out=False)

    result = netflix_titles_schema.dump(netflix_titles.items)
    return jsonify(result)

# Get single Netflix Title
@app.route('/netflix/<show_id>', methods=['GET'])
def get_netflix_title(show_id):
    netflix_title = Netflix.query.get(show_id)
    if netflix_title:
        return netflix_title_schema.jsonify(netflix_title)
    else:
        message = 'Show ID {} not found'.format(show_id)
        return jsonify({'Message': message})

# Create a New Netflix Title
@app.route('/netflix', methods=['POST'])
def add_netflix_title():

    show_id = request.json['show_id']
    show_type = request.json['show_type']
    title = request.json['title']
    director = request.json['director']
    cast = request.json['cast']
    country = request.json['country']
    date_added = request.json['date_added']
    release_year = request.json['release_year']
    rating = request.json['rating']
    duration = request.json['duration']
    listed_in = request.json['listed_in']
    description = request.json['description']

    try:
        new_netflix_title = Netflix(show_id, show_type, title, director, cast, country, date_added, release_year,
                                    rating, duration, listed_in, description)

        db.session.add(new_netflix_title)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        logging.exception("Error adding a new netflix title: %s", e)
        abort(500, 'Error adding a new netflix title')
    else:
        return netflix_title_schema.jsonify(new_netflix_title)

# Update a Netflix Title
@app.route('/netflix/<show_id>', methods=['PUT'])
def update_netflix_title(show_id):
    netflix_title = Netflix.query.get(show_id)

    if netflix_title:
        show_type = request.json['show_type']
        title = request.json['title']
        director = request.json['director']
        cast = request.json['cast']
        country = request.json['country']
        date_added = request.json['date_added']
        release_year = request.json['release_year']
        rating = request.json['rating']
        duration = request.json['duration']
        listed_in = request.json['listed_in']
        description = request.json['description']

        try:
            netflix_title.show_type = show_type
            netflix_title.title = title
            netflix_title.director = director
            netflix_title.cast = cast
            netflix_title.country = country
            netflix_title.date_added = date_added
            netflix_title.release_year = release_year
            netflix_title.rating = rating
            netflix_title.duration = duration
            netflix_title.listed_in = listed_in
            netflix_title.description = description

            db.session.commit()
        except exc.SQLAlchemyError as e:
            logging.exception("Error updating an existing netflix title: %s", e)
            abort(500, 'Error updating an existing netflix title')
        else:
            return netflix_title_schema.jsonify(netflix_title)
    else:
        message = 'Show ID {} not found hence no data has been updated'.format(show_id)
        return jsonify({'Message': message})


# Delete a Netflix Title
@app.route('/netflix/<show_id>', methods=['DELETE'])
def delete_product(show_id):
    netflix_title = Netflix.query.get(show_id)

    if netflix_title:
        try:
            db.session.delete(netflix_title)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            logging.exception("Error deleting an existing netflix title: %s", e)
            abort(500, 'Error deleting an existing netflix title')
        else:
            return netflix_title_schema.jsonify(netflix_title)
    else:
        message = 'Show ID {} not found hence no data has been deleted'.format(show_id)
        return jsonify({'Message': message})
