import unittest
import json

from flaskapp.config import app


class NetflixTitleTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app = app.test_client()

    def test_add_netflix_title(self):
        payload = json.dumps({
            "show_id": 80125930,
            "show_type": "Movie",
            "title": "#realityhigh",
            "director": "Fernando Lebrija",
            "cast": "Nesta Cooper, Kate Walsh, John Michael Higgins, Keith Powers, Alicia Sanz, Jake Borelli, Kid Ink",
            "country": "United States, India, South Korea, China",
            "date_added": "8-Sep-17",
            "release_year": 2017,
            "rating": "TV-14",
            "duration": "99 min",
            "listed_in": "Comedies",
            "description": "When nerdy high schooler Dani finally attracts the interest of her longtime crush."
        })
        response = self.app.post('/netflix', headers={"Content-Type": "application/json"}, data=payload)
        expected_response = {
            "cast": "Nesta Cooper, Kate Walsh, John Michael Higgins, Keith Powers, Alicia Sanz, Jake Borelli, Kid Ink",
            "country": "United States, India, South Korea, China",
            "date_added": "8-Sep-17",
            "description": "When nerdy high schooler Dani finally attracts the interest of her longtime crush.",
            "director": "Fernando Lebrija",
            "duration": "99 min",
            "listed_in": "Comedies",
            "rating": "TV-14",
            "release_year": 2017,
            "show_id": 80125930,
            "show_type": "Movie",
            "title": "#realityhigh"
        }

        self.assertEqual(expected_response, json.loads(response.data))

    def test_get_netflix_titles(self):
        response = self.app.get("/netflix")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        expected_response = [{
            "cast": "Nesta Cooper, Kate Walsh, John Michael Higgins, Keith Powers, Alicia Sanz, Jake Borelli, Kid Ink",
            "country": "United States, India, South Korea, China",
            "date_added": "8-Sep-17",
            "description": "When nerdy high schooler Dani finally attracts the interest of her longtime crush.",
            "director": "Fernando Lebrija",
            "duration": "99 min",
            "listed_in": "Comedies",
            "rating": "TV-14",
            "release_year": 2017,
            "show_id": 80125930,
            "show_type": "Movie",
            "title": "#realityhigh"
        }]
        self.assertEqual(expected_response, json.loads(response.data))

    def test_error_filter_by_field(self):
        response = self.app.get("/netflix?filter_by_field=cast")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            {"message": "If you are filtering according to a column specify search criteria with search QS param"},
            json.loads(response.data))
        response = self.app.get("/netflix?filter_by_field=director1&search=Fer")
        self.assertEqual(
            {"message": "filter_by_field passed is not a valid column in Netflix Model"},
            json.loads(response.data))

    def test_error_sort_by_field(self):
        response = self.app.get("/netflix?sort_by_field=director1")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual({"message": "Sort_by_field passed is not a valid column in Netflix Model"},
                         json.loads(response.data))

    def test_get_netflix_title(self):
        response = self.app.get("/netflix/80125930")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        expected_response = {
            "cast": "Nesta Cooper, Kate Walsh, John Michael Higgins, Keith Powers, Alicia Sanz, Jake Borelli, Kid Ink",
            "country": "United States, India, South Korea, China",
            "date_added": "8-Sep-17",
            "description": "When nerdy high schooler Dani finally attracts the interest of her longtime crush.",
            "director": "Fernando Lebrija",
            "duration": "99 min",
            "listed_in": "Comedies",
            "rating": "TV-14",
            "release_year": 2017,
            "show_id": 80125930,
            "show_type": "Movie",
            "title": "#realityhigh"
        }
        self.assertEqual(expected_response, json.loads(response.data))

    def test_no_show_id_get_netflix_title(self):
        response = self.app.get("/netflix/1")
        self.assertEqual({'Message': 'Show ID 1 not found'}, json.loads(response.data))

    def test_update_netflix_title(self):
        payload = json.dumps({
            "show_type": "Movie",
            "title": "#realityhigh updated",
            "director": "Fernando Lebrija",
            "cast": "Nesta Cooper, Kate Walsh, John Michael Higgins, Keith Powers, Alicia Sanz, Jake Borelli, Kid Ink",
            "country": "United States, India, South Korea, China",
            "date_added": "8-Sep-17",
            "release_year": 2017,
            "rating": "TV-14",
            "duration": "99 min",
            "listed_in": "Comedies updated",
            "description": "When nerdy high schooler Dani finally attracts the interest of her longtime crush."
        })
        response = self.app.put('/netflix/80125930', headers={"Content-Type": "application/json"}, data=payload)
        expected_response = {
            "cast": "Nesta Cooper, Kate Walsh, John Michael Higgins, Keith Powers, Alicia Sanz, Jake Borelli, Kid Ink",
            "country": "United States, India, South Korea, China",
            "date_added": "8-Sep-17",
            "description": "When nerdy high schooler Dani finally attracts the interest of her longtime crush.",
            "director": "Fernando Lebrija",
            "duration": "99 min",
            "listed_in": "Comedies updated",
            "rating": "TV-14",
            "release_year": 2017,
            "show_id": 80125930,
            "show_type": "Movie",
            "title": "#realityhigh updated"
        }

        self.assertEqual(expected_response, json.loads(response.data))

    def test_delete_netflix_title(self):
        # Creating a record just for testing deletion.
        payload = json.dumps({
            "show_id": 1,
            "show_type": "Sample Movie",
            "title": "Sample Title",
            "director": "Sample Director",
            "cast": "Sample Cast",
            "country": "United States",
            "date_added": "8-Sep-17",
            "release_year": 2017,
            "rating": "TV-14",
            "duration": "99 min",
            "listed_in": "Comedies",
            "description": "Sample record just for deletion"
        })
        self.app.post('/netflix', headers={"Content-Type": "application/json"}, data=payload)
        response = self.app.delete('/netflix/1', headers={"Content-Type": "application/json"})
        expected_response = {
            "show_id": 1,
            "show_type": "Sample Movie",
            "title": "Sample Title",
            "director": "Sample Director",
            "cast": "Sample Cast",
            "country": "United States",
            "date_added": "8-Sep-17",
            "release_year": 2017,
            "rating": "TV-14",
            "duration": "99 min",
            "listed_in": "Comedies",
            "description": "Sample record just for deletion"
        }

        self.assertEqual(expected_response, json.loads(response.data))


if __name__ == '__main__':
    unittest.main()
