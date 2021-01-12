# Netflix API with Flask + SqlAlchemy + Marshmallow

This is simple API built to fetch, create, update and delete Netflix Data.

This current application is hosted on Google App Engine and connected to Google Cloud SQL.

Best to use _**POSTMAN**_ for testing.

**Hosted URL** - https://<project_id>.uc.r.appspot.com/netflix

If you are cloning the repository and running the app or unit/integrations tests _in-memory sqllite_ would be used.

_**Example for running the unit tests in local:**_

```python -m unittest flaskapp/netflix_title_test.py```

## GET or Fetching the data 
- https://{hostname}/netflix
- https://{hostname}/netflix/show_id

### Functionalities supported: 
- Get all data
- Get a single record based on show_id
- Ability to search on any column with a search string
- Filter data based on a column and search string
- Ability to sort on any column ascending or descending
- Pagination with support for each page & size

#### Supported Query String Params:
1) page & size - Accepts only integers and used to display number of records in each fetch. By default if nothing is passed returns first 20 records.
2) search - Accepts a value and searches in all the columns of Netflix Model.
3) filter_by_field - Used to filter records based on a specific column in Netflix Model. 'search' QS param has to be used in conjunction.
4) sort_by_field - Used to sort records based on a specific column in Netflix Model. By default if nothing is passed would pickup show_id for sorting.
5) sort_order - Sort order expected. By default it would sort ascending.

**Sample URL Example** - https://netflix-titles-301202.uc.r.appspot.com/netflix?search=Preeti&filter_by_field=cast&sort_by_field=release_year&sort_order=desc

## POST or Creating/Inserting the data 
- https://{hostname}/netflix

### Functionalities supported: 
- Insert data into the database

**Sample JSON Body**:
```
    {
    "cast": "Sample Cast",
    "country": "United States",
    "date_added": "8-Sep-17",
    "description": "Sample description",
    "director": "Sample director",
    "duration": "99 min",
    "listed_in": "Comedies",
    "rating": "TV-14",
    "release_year": 2017,
    "show_id": 1,
    "show_type": "Movie",
    "title": "Sample Title"
    }
```

## PUT or Updating the data 
- https://{hostname}/netflix/{show_id}

### Functionalities supported: 
- Update data in the database based on show_id

**Sample JSON Body**:
```
    {
    "cast": "Sample Cast Updated",
    "country": "United States",
    "date_added": "8-Sep-17",
    "description": "Sample description Updated",
    "director": "Sample director Updated",
    "duration": "99 min",
    "listed_in": "Comedies",
    "rating": "TV-14",
    "release_year": 2017,
    "show_type": "Movie",
    "title": "Sample Title"
    }
```

## DELETE or Deleting the data 
- https://{hostname}/netflix/{show_id}

### Functionalities supported: 
- Delete data in the database based on show_id


